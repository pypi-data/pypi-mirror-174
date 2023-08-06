import argparse
import os
import sys

sys.path.append('../../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import datetime
from dateutil.tz import gettz
from zeno_etl_libs.db.db import DB, PostGreWrite

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stag, prod)")

args, unknown = parser.parse_known_args()

env = args.env
os.environ['env'] = env
logger = get_logger()

rs_db = DB()
rs_db.open_connection()
s3 = S3()

schema = 'prod2-generico'
table_name = 'store-ops-metrics'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

date1= (datetime.datetime.today() + relativedelta(months=-1)).replace(day=1).strftime('%Y-%m-%d')
date2= (datetime.datetime.today() + relativedelta(days=-1)).strftime('%Y-%m-%d')

# =============================================================================
# Importing all stores with opening date
# =============================================================================

sm = """
       select
        sm.id as "store-id"
    from
        "prod2-generico"."stores-master" sm
    inner join "prod2-generico"."stores" s on
        s.id = sm.id
    where
        date(sm."opened-at") != '0101-01-01'
        and s."is-active" = 1
    group by
        sm.id;
"""
sm_data = rs_db.get_df(sm)
sm_data.columns = [c.replace('-', '_') for c in sm_data.columns]

sm_data['join']='A'

# =============================================================================
# Date range explode
# =============================================================================
d_date = pd.DataFrame({'join':['A']})
#d_date['join']='A'
d_date['start_date']= date1
d_date['end_date']= date2
d_date['date'] = [pd.date_range(s, e, freq='d') for s, e in
                         zip(pd.to_datetime(d_date['start_date']),
                             pd.to_datetime(d_date['end_date']))]
#d_date = d_date.explode('date')
d_date = pd.DataFrame({'date': np.concatenate(d_date.date.values)})
d_date['join']='A'

#d_date.drop(['start_date','end_date'],axis=1,inplace=True)

d_date['date'] = d_date['date'].astype('str')

m_data = pd.merge(left=sm_data,right=d_date,on=['join'],how='inner')
m_data.drop('join',axis=1,inplace=True)

# =============================================================================
# AS PR received TAT
# =============================================================================

as_pr = f"""
    select
	"store-id" ,
	date("received-at") as "date",
	avg( case when (sb."auto-short" = 0 AND sb."auto-generated" = 0 AND sb."status" NOT IN ('deleted')) then (datediff('hour', sd."store-delivered-at", sb."received-at")) end) as "pr_received_tat",
	avg( case when (sb."auto-short" = 1 and sb."home-delivery" = 0 and sb."patient-id" = 4480 and sb."status" NOT IN ('deleted')) then (datediff('hour', sd."store-delivered-at", sb."received-at")) end) as "as_received_tat"
from
	"prod2-generico"."short-book-1" sb
left join "prod2-generico"."store-delivered" sd on
	sd.id = sb.id
where
	date("received-at")>= '{date1}'
    and date("received-at")<= '{date2}'
group by
	"store-id" ,
	date("received-at");
"""
as_pr_tat = rs_db.get_df(as_pr)

as_pr_tat.columns = [c.replace('-', '_') for c in as_pr_tat.columns]

as_pr_tat['date'] = as_pr_tat['date'].astype('str')
m_data = pd.merge(left=m_data,right=as_pr_tat,how='left',on=['store_id','date'])

# =============================================================================
# Audit Loss
# =============================================================================

a_loss = f"""
    select
	a."inventory-date" as "date",
	a."store-id",
	sum(b.expected*b."final-ptr") as "expected-ptr",
	sum(b."final-ptr" *(b.expected-b.accounted)) as "loss-ptr"
from
	"prod2-generico"."inventory-check-1" a
join "prod2-generico"."inventory-check-items-1" b on
	a.id = b."check-id"
where
	a."type" = 'daily-audit'
	and date(a."created-at") >= '{date1}'
	and date(a."created-at") <= '{date2}'
	and b."expected" > 0
group by
	1,
	2;
"""
audit_loss = rs_db.get_df(a_loss)
audit_loss.columns = [c.replace('-', '_') for c in audit_loss.columns]
audit_loss['date'] = audit_loss['date'].astype('str')

m_data = pd.merge(left=m_data,right=audit_loss,on=['store_id','date'],how='left')

# =============================================================================
# LP Liquidation + LP PR PCT
# =============================================================================

lp = f"""
    select
	lp."store-id" ,
	lp."received-date" as "date",
	sum(lp."lp-sales-sum") as "lp-sales-sum",
	sum(lp."lp-value-sum") as "lp-value",
	sum(case when s."pr-flag"=True then s."revenue-value" end) as "lp_pr_sales"
from
	"prod2-generico"."lp-liquidation" lp
inner join "prod2-generico"."sales" s on
	s."store-id" = lp."store-id"
	and s."created-date" = lp."received-date"
    where date(lp."received-date")>= '{date1}'
    and date(lp."received-date")<= '{date2}'
group by
	lp."store-id" ,
	date(lp."received-date");
"""
lp_liq = rs_db.get_df(lp)
lp_liq.columns = [c.replace('-', '_') for c in lp_liq.columns]
lp_liq['date'] = lp_liq['date'].astype('str')

m_data = pd.merge(left=m_data,right=lp_liq,on=['store_id','date'],how='left')


# =============================================================================
# OOS less than min + STore level OOS
# =============================================================================

oos = f"""
    select
	oos."closing-date" as "date",
	oos."store-id" ,
	sum( case when oos."bucket" in ('AW', 'AX', 'AY') and oos."oos-min-count" = 0 then oos."drug-count" end) as min_count_oos_ax,
	sum(case when oos."bucket" in ('AW', 'AX', 'AY') then oos."drug-count" end) as "total_drug_count_oos_ax",
	sum(case when oos."oos-min-count" = 0 and d."company-id" = 6984 then oos."drug-count" end) as "goodaid_min_count",
	sum(case when d."company-id" = 6984 then oos."drug-count" end) as "goodaid_total_count",
	sum(oos."drug-count") as "total_drug_count_oos",
	sum(oos."oos-count") as "total_oos_drug_count_oos"
from
	"prod2-generico"."out-of-shelf-drug-level" oos
inner join "prod2-generico"."drugs" d on
	oos."drug-id" = d."id"
where
	oos."max-set" = 'Y'
    and oos."mature-flag" = 'Y'
    and date(oos."closing-date") >='{date1}'
    and date(oos."closing-date") <='{date2}'
group by
	1,
	2;
"""
oos_data = rs_db.get_df(oos)
oos_data.columns = [c.replace('-', '_') for c in oos_data.columns]
oos_data['date'] = oos_data['date'].astype('str')

m_data = pd.merge(left=m_data,right=oos_data,on=['store_id','date'],how='left')

# =============================================================================
# Feedback rating and bill pct
# =============================================================================

fb = f"""
    select
	date(b."created-at") as "date",
	b."store-id",
	count(distinct case when f.rating is not null then b.id end)* 1.0 / count(distinct b.id)* 1.0 as "feedback-bills-pct",
	NVL(count(distinct case when f.rating in (1, 2) then b.id end),
	0) as "flag-rating"
from
	"prod2-generico"."bills-1" b
left join "prod2-generico"."feedback" f on
	f."bill-id" = b.id
    where date(b."created-at") >= '{date1}' 
    and date(b."created-at") <= '{date2}'
group by
	date(b."created-at") ,
	b."store-id";
"""
fb_data = rs_db.get_df(fb)
fb_data.columns = [c.replace('-', '_') for c in fb_data.columns]
fb_data['date'] = fb_data['date'].astype('str')

m_data = pd.merge(left=m_data,right=fb_data,on=['store_id','date'],how='left')


# =============================================================================
# Sales related Metric
# =============================================================================

sd = f"""
   select
	"store-id",
	"created-date" as "date",
	sum(case when "substitution-status" = 'substituted' then quantity end) as "subs_num",
    NVL(sum(case when "substitution-status" in ('substituted', 'not-substituted') then quantity end),1) as "subs_den",
	sum(case when "substitution-status" = 'substituted' and "hd-flag" = True then quantity end) as "hd_subs_num",
    NVL(sum(case when "substitution-status" in ('substituted', 'not-substituted') and "hd-flag" = True then quantity end),1) as "hd_subs_den",
	sum(case when "substitution-status-g" = 'ga-substituted' then quantity end) as "ga_subs_num",
    NVL(sum(case when "substitution-status" in ('ga-substituted', 'substituted', 'not-substituted') then quantity end),1) as "ga_subs_den",
	sum(case when "bill-flag" = 'return' then "revenue-value" end)  as "return-value",
    sum(case when "bill-flag" = 'gross' then "revenue-value" end) as "gross-revennue",
	count(distinct case when "promo-code" = 'BOGO' and "bill-flag" = 'gross' then "bill-id" end) as "bogo-bills",
	sum("revenue-value") as revenue,
	sum(case when "pr-flag" =True then "revenue-value" end) as "pr_sales",
	sum(case when "hd-flag" =True then "revenue-value" end) as "hd_sales",
	sum(case when "company-id" =6984 then "revenue-value" end) as "goodaid_sales",
	sum(case when "ecom-flag" =True then "revenue-value" end) as "ecomm_sales",
	count(DISTINCT case when "hd-flag" =True and "bill-flag" = 'gross' then "bill-id" end) as "hd_bills",
	count(distinct case when "bill-flag" = 'gross' then "bill-id" end) as "NOB",
	sum(case when "bill-flag" = 'gross' then "revenue-value" end)*1.0/NVL(count(distinct case when "bill-flag" = 'gross' then "bill-id" end),1)*1.0 as "ABV"
from
	"prod2-generico"."sales"
    where "created-date">='{date1}'
    and "created-date"<='{date2}'
group by
	"store-id" ,
	"created-date";
"""
sales_data = rs_db.get_df(sd)
sales_data.columns = [c.replace('-', '_') for c in sales_data.columns]
sales_data['date'] = sales_data['date'].astype('str')

m_data = pd.merge(left=m_data,right=sales_data,on=['store_id','date'],how='left')


# =============================================================================
# Missed Call info
# =============================================================================

msc = f"""
   SELECT
	scle."store-id",
	date(scle."date-time") as "date",
	count(case when scle."call-type" = 'MISSED' then scle."call-type" end) as "missed_calls",
	count(scle."call-type") as "total_received_calls"
FROM
	"prod2-generico"."store-call-logs-entries" scle
where
	scle."call-type" in ('INCOMING',
	'MISSED')
	and date(scle."date-time") >= '{date1}'
    and date(scle."date-time") <= '{date2}'
group by
	scle."store-id",
    date(scle."date-time");
"""
missed_call = rs_db.get_df(msc)
missed_call.columns = [c.replace('-', '_') for c in missed_call.columns]
missed_call['date'] = missed_call['date'].astype('str')

m_data = pd.merge(left=m_data,right=missed_call,on=['store_id','date'],how='left')


# =============================================================================
# Calling dashboard
# =============================================================================

call = f"""
  select
	cd."store-id" ,
	date(cd."created-at") as "date",
	count(distinct cd.id) as "target_calls",
	count(distinct case when ch.id is not null then cd.id end) as "actual_calls"
from
	"prod2-generico"."calling-dashboard" cd
left join "prod2-generico"."calling-history" ch on
	cd.id = ch."calling-dashboard-id"
where
	date(cd."created-at")>= '{date1}'
    and date(cd."created-at")<= '{date2}'
group by
	cd."store-id" ,
	date(cd."created-at");
"""
calling_data = rs_db.get_df(call)
calling_data.columns = [c.replace('-', '_') for c in calling_data.columns]
calling_data['date'] = calling_data['date'].astype('str')

m_data = pd.merge(left=m_data,right=calling_data,on=['store_id','date'],how='left')


# =============================================================================
# NPI
# =============================================================================

npi = f"""
  select
	nrt."store-id" ,
	date(nrt."store-return-created-at") as "date",
	avg(DATEDIFF ('h', nrt."npi-added-in-store-at", nrt."check-created-at" )) as "hours-to-start-scanning",
	avg(DATEDIFF ('h', nrt."npi-added-in-store-at", nrt."store-return-created-at" )) as "hours-to-mark-store-return"
from
	"prod2-generico"."npi-returns-tracking" nrt
    where date(nrt."store-return-created-at")>='{date1}'
    and date(nrt."store-return-created-at")<= '{date2}'
group by
	nrt."store-id",
	date(nrt."store-return-created-at");
"""
npi_data = rs_db.get_df(npi)
npi_data.columns = [c.replace('-', '_') for c in npi_data.columns]
npi_data['date'] = npi_data['date'].astype('str')

m_data = pd.merge(left=m_data,right=npi_data,on=['store_id','date'],how='left')


# =============================================================================
# Cluster FF
# =============================================================================

cff = f"""
  Select
	date(pso."created-at") AS "date",
	-- PSO Created at
 	pstm."from-store-id" AS "store-id" ,
	--pstm."to-store-id" AS "destination-store-id",
	--	max(c.id) as "cluster-id" ,
	--	max(sos."name") AS "source_store",
	--	max(des."name") AS "destination_store",
	--	max(pstm."item-quantity") AS "to-be-transferred-qty",
	--	SUM(sti."quantity") as "actual-transferred-qty",
	--	pso."status" as "pso-status",
	--	pstm."status" AS "tn-status",
	--	st."status" AS "st-status",
	--	pso."drug-id" ,
	--	pso."drug-name" ,
	--	max(pstm.id) AS "pstm-id",
	--	max(pstm."is-active") as  "is-active",
 	avg(DATEDIFF ('h', pstm."created-at", st."initiated-at" )) as "hrs_cluster_order_ready_for_pickup",
	avg(DATEDIFF ('h', pstm."created-at", st."transferred-at" )) as "hrs_cluster_biker_picked_up_order",
	avg(DATEDIFF ('h', pstm."created-at", st."received-at" )) as "hrs_cluster_store_received_order" 
	-- PSO Created at
	FROM "prod2-generico"."pso-stock-transfer-mapping" pstm
LEFT JOIN "prod2-generico"."stock-transfers-1" st on
	pstm."stock-transfer-id" = st.id
Left JOIN "prod2-generico"."pso-stock-transfer-inventory-mapping" pstim ON
	pstm.id = pstim."pso-stock-transfer-mapping-id"
LEFT JOIN "prod2-generico"."stock-transfer-items-1" sti ON
	pstim."inventory-id" = sti."inventory-id"
	AND st.id = sti."transfer-id"
Left join "prod2-generico"."patients-store-orders" pso ON
	pstm."patient-store-order-id" = pso.id
left join "prod2-generico"."store-clusters" sc on
	pstm."from-store-id" = sc."store-id"
left join "prod2-generico".stores sos on
	pstm."from-store-id" = sos.id
left join "prod2-generico".stores des on
	pstm."to-store-id" = des.id
inner join "prod2-generico".clusters c on
	sc."cluster-id" = c.id
	and sc."is-active" = 1
WHERE
	sc."cluster-id" is not null
	AND date(pso."created-at") >= '{date1}'
    and date(pso."created-at") <= '{date2}'
	GROUP BY pstm."from-store-id",
	date(pso."created-at");
"""
cluster_data = rs_db.get_df(cff)
cluster_data.columns = [c.replace('-', '_') for c in cluster_data.columns]
cluster_data['date'] = cluster_data['date'].astype('str')

m_data = pd.merge(left=m_data,right=cluster_data,on=['store_id','date'],how='left')


# =============================================================================
# as - pr otif
# =============================================================================

aspr = f"""
  select
	"store-id" ,
	date("created-at") as "date",
	sum(case
		when "as-ms-pr" = 'as' then "requested-quantity"
	end) as "as_requested_qty",
	sum(case
		when "as-ms-pr" = 'pr' then "requested-quantity"
	end) as "pr_requested_qty",
	sum(case
		when "as-ms-pr" = 'as'
		and date("store-delivered-at")!= '0101-01-01'
		and "store-delivered-at" < "delivery-tat" then "requested-quantity"
	end) as "as_otif_qty",
	sum(case
		when "as-ms-pr" = 'pr'
		and date("store-delivered-at")!= '0101-01-01'
		and "store-delivered-at" < "delivery-tat" then "requested-quantity"
	end) as "pr_otif_qty"
from
	"prod2-generico"."sb-sla"
	where date("created-at")>='{date1}'
    and date("created-at")<= '{date2}'
	group by "store-id" ,date("created-at");
"""
aspr_data = rs_db.get_df(aspr)
aspr_data.columns = [c.replace('-', '_') for c in aspr_data.columns]
aspr_data['date'] = aspr_data['date'].astype('str')

m_data = pd.merge(left=m_data,right=aspr_data,on=['store_id','date'],how='left')


# =============================================================================
# store opening closing
# =============================================================================
s_date = f"""
  select
	date("created-at") as "date",
	"store-id" ,
	min("created-at") as "first_search",
	max("created-at") as "last_search"
from
	"prod2-generico"."searches"
group by
	date("created-at"),
	"store-id";
"""
opening_data = rs_db.get_df(s_date)
opening_data.columns = [c.replace('-', '_') for c in opening_data.columns]
opening_data['date'] = opening_data['date'].astype('str')

m_data = pd.merge(left=m_data,right=opening_data,on=['store_id','date'],how='left')

# =============================================================================
# store info
# =============================================================================

s_info = f"""

select
	id as "store-id",
	store ,
	"line-manager" ,
	abo ,
	city ,
	"franchisee-name",
	acquired ,
	"cluster-name" ,
	"old-new-static"
from
	"prod2-generico"."stores-master";
"""
store_info = rs_db.get_df(s_info)
store_info.columns = [c.replace('-', '_') for c in store_info.columns]

m_data = pd.merge(left=m_data,right=store_info,on=['store_id'],how='left')


pro = f"""
  Select
	pr."store-id" ,
	date(pr."created-at") as "date",
	sum(pr."selling-rate") as "pr_created_value",
	sum(case when (case when pr."order-type" = 'pickup' then pr."completed-at" else hdm."delivered-at" end)<= pr."turnaround-time" then pr."selling-rate" else 0 end) as "within_slot_delivered_pr_value",
	sum(case when (case when pr."order-type" = 'pickup' then pr."completed-at" else hdm."delivered-at" end) is not null then pr."selling-rate" end) as "total_delivered_pr_value"
from
	"prod2-generico"."patient-requests-metadata" pr
	left join "prod2-generico"."home-delivery-metadata" hdm
on hdm.id =pr.id 
where date(pr."created-at") >= '{date1}' and date(pr."created-at") <= '{date2}'
	group by
	1,2;
"""
pro_data = rs_db.get_df(pro)
pro_data.columns = [c.replace('-', '_') for c in pro_data.columns]
pro_data['date'] = pro_data['date'].astype('str')


m_data = pd.merge(left=m_data,right=pro_data,on=['store_id','date'],how='left')

m_data.info()
# Write to Redshift Also
m_data.columns = [c.replace('_', '-') for c in m_data.columns]

truncate_query = f''' DELETE FROM "{schema}"."{table_name}" '''
rs_db.execute(truncate_query)

s3.write_df_to_db(df=m_data[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)

# Closing the DB Connection
rs_db.close_connection()

