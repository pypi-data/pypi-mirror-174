"""
Author : shubham.gupta@zeno.health
Purpose : Store Intelligence and Daily recommendation
"""

# Essential Libraries

from datetime import date, timedelta
# Warnings
from warnings import filterwarnings as fw

import pandas as pd

fw('ignore')

import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB, MySQL
from zeno_etl_libs.helper.email.email import Email

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="shubham.gupta@zeno.health", type=str, required=False)
parser.add_argument('-debug', '--debug_mode', default='Y', type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

# parameters
email_to = args.email_to
debug = args.debug_mode

logger = get_logger()
logger.info(f"env: {env}")

rs_db = DB(read_only=True)
rs_db.open_connection()

s3 = S3()
read_schema = "prod2-generico"
email = Email()


################################################################
###################### Helper Functions ########################
################################################################


def store_info_func(store_id):
    """
    This basic function return store name and emails
    """
    rs_db_h = DB(read_only=True)
    rs_db_h.open_connection()

    store_q = f"""select
                    "name" as "store-name",
                    email as "email-1",
                    "email-2" as "email-2",
                    "franchisee-email" as "email-3"
                from
                    "prod2-generico".stores s
                where
                    id = {store_id};
            """
    store_info = rs_db.get_df(store_q)
    store_info = store_info.iloc[0]
    store_name = store_info["store-name"]
    store_mails = [store_info["email-1"], store_info["email-2"], store_info["email-3"]]
    return store_name, store_mails


#################################################################
###################### OOS and Inventory ########################
#################################################################

oos_q = f"""
        select
            t_final.*,
            d."drug-name" as "drug-name"
        from
            (
            select
                t."store-id",
                t."drug-id",
                min(t."closing-date") "from-date",
                max(t."closing-date") "to-date",
                datediff('days', min(t."closing-date"), max(t."closing-date")) + 1 as "days-count"
            from
                (
                select
                    * ,
                    row_number() over (partition by "store-id",
                    "drug-id"
                order by
                    "closing-date" desc) as "rn",
                    dateadd('days',
                    "rn",
                    "closing-date") "plus-date"
                from
                    "{read_schema}"."out-of-shelf-drug-level" oosdl
                where
                    "oos-count" = 1
                    and "max-set" = 'Y'
                    and "mature-flag" = 'Y') t
            where
                date("plus-date") = current_date
            group by
                t."store-id",
                t."drug-id"
            having
                "days-count" > 5) t_final
        left join 
            "{read_schema}".stores s on
            t_final."store-id" = s.id
        left join 
            "{read_schema}".drugs d on
            t_final."drug-id" = d.id;
        """

sales_loss_q = f"""
                select 	
                    tw."store-id",
                    tw."drug-id",
                    min(tw."closing-date") "from-date",
                    max(tw."closing-date") "to-date",
                    datediff('days', min(tw."closing-date"), max(tw."closing-date")) + 1 as "days-count",
                    sum(s."revenue-value") as "total-sales"
                from
                    (
                    select
                        *,
                        rank() over (partition by "store-id",
                        "drug-id"
                    order by
                        "plus-date" desc) as "latest-rank"
                    from
                        (
                        select
                            * ,
                            row_number() over (partition by "store-id",
                            "drug-id"
                        order by
                            "closing-date" desc) as "rn",
                            dateadd('days',
                            "rn",
                            "closing-date") "plus-date"
                        from
                             "{read_schema}"."out-of-shelf-drug-level" oosdl
                        where
                            "oos-count" = 0) t ) tw
                left join  "{read_schema}".sales s on
                    date(s."created-at") = tw."closing-date"
                    and s."drug-id" = tw."drug-id"
                    and s."store-id" = tw."store-id"
                where 
                    "latest-rank" = 1
                    and "plus-date" != current_date
                group by 
                    tw."store-id",
                    tw."drug-id";
                """

oos = rs_db.get_df(oos_q)
sales_loss = rs_db.get_df(sales_loss_q)

sales_loss['avg-per-day-sales'] = sales_loss['total-sales'] / sales_loss['days-count']
sales_loss = sales_loss[['store-id', 'drug-id', 'avg-per-day-sales']]
oos = pd.merge(oos, sales_loss, how='left', on=['store-id', 'drug-id'])
oos = oos.dropna(subset=['avg-per-day-sales'])
oos['sales-loss'] = oos['avg-per-day-sales'] * oos['days-count']

# Let's solve issues for top 20 only for a day

oos = oos.sort_values('sales-loss', ascending=False).head(20)
store_ids = oos['store-id'].unique()

for store_id in store_ids:
    store_name, store_emails = store_info_func(store_id)
    if debug == 'Y':
        store_emails = ['shubham.gupta@zeno.health']
    else:
        store_emails.append(email_to)
    oos_mail_body = f"""
    Hey {store_name} Store,
    There are some drugs which are out of stock on your store since very long time
    
    Possible issues are as listed :
    
    1. Auto Short not triggerd
    2. Short in market 
    3. Quantity in locked state (Store inventory)
    
    Because of these specific drugs OOS of your store is high
    Your daily task for today is resolve these issues :
    
    1. Check inventory lock status of mentioned drugs and unlock the status
    
    2. If these drugs are short in market then contact Supply chain team / Data Science team to change status of "Max-Set"
    till the time it gets available in market, substitute it with alternatives
    
    3. In case auto-short is not triggered, Order it manually (Manual Short)
    """

    file_name = 'OOS_Drugs.xlsx'
    file_path = s3.write_df_to_excel(data={'Drugs': oos[oos['store-id'] == store_id]}, file_name=file_name)
    email.send_email_file(subject="Store Daily Task 1 : Unavailability Issue",
                          mail_body=oos_mail_body,
                          to_emails=store_emails,
                          file_uris=[],
                          file_paths=[file_path])

inv_q = f"""
        select
            "store-id",
            "drug-id",
            sum(quantity) as "quantity",
            sum("locked-quantity") as "locked-quantity",
            sum("locked-for-check") as "locked-for-check",
            sum("locked-for-audit") as "locked-for-audit",
            sum("locked-for-return") as "locked-for-return",
            sum("locked-for-transfer") as "locked-for-transfer",
            sum("extra-quantity") as "extra-quantity",
            max("updated-at") as "updated-at"
        from
            "{read_schema}"."inventory-1" i
        group by
            "store-id",
            "drug-id"
        having 
            sum("quantity") = 0
            and sum("locked-quantity" + "locked-for-check" + "locked-for-audit" + "locked-for-return" + "locked-for-transfer" + "extra-quantity") > 0
            and max("updated-at") <= current_date - 2;
        """
inv = rs_db.get_df(inv_q)
# Top 10 Stores
store_ids = inv.groupby('store-id')['drug-id'].nunique().sort_values(ascending=False)[:10].index

for store_id in store_ids:
    store_name, store_emails = store_info_func(store_id)
    if debug == 'Y':
        store_emails = ['shubham.gupta@zeno.health']
    else:
        store_emails.append(email_to)
    inv_mail_body = f"""
    Hey {store_name} Store,
    There are some drugs where available quantity is 0 but quantity stuck in locked state
    since long time which cause trouble in triggering Auto Short 

    Your daily task for today is resolve these issues :

    > Unlock mentioned drugs 
    
    """

    file_name = 'Locked State Drugs.xlsx'
    # 10 Drugs a day
    file_path = s3.write_df_to_excel(data={'Drugs': inv[inv['store-id'] == store_id].head(10)}, file_name=file_name)
    email.send_email_file(subject="Store Daily Task 2 : Inventory locked state Issue",
                          mail_body=inv_mail_body,
                          to_emails=store_emails,
                          file_uris=[],
                          file_paths=[file_path])

#################################################################
###################### Substitution  ############################
#################################################################

gen_shift_q = """
                select
                    "primary-store-id" as "store-id",
                    (case
                        when "post-generic-quantity" > 0 then 'generic-shift'
                        when "post-generic-quantity" = 0
                        and "post-ethical-quantity" > 0 then 'still-ethical'
                        else 'bought others'
                    end
                    ) "behaviour-shift",
                    count(distinct t1."patient-id") "patient-count"
                from
                    (
                    select
                        "patient-id",
                        sum("quantity-ethical") "pre-ethical-quantity",
                        sum("quantity-generic") "pre-generic-quantity"
                    from
                        "prod2-generico"."retention-master" rm
                    where
                        "created-at" < date_trunc('month', current_date)
                        and "created-at" >= dateadd('month',
                        -3,
                        date_trunc('month', current_date))
                    group by
                        "patient-id"
                    having
                        "pre-ethical-quantity" > 0
                        and "pre-generic-quantity" = 0 ) t1
                inner join
                (
                    select
                        "patient-id",
                        "primary-store-id",
                        sum("quantity-ethical") "post-ethical-quantity",
                        sum("quantity-generic") "post-generic-quantity"
                    from
                        "prod2-generico"."retention-master" rm
                    where
                        "created-at" >= date_trunc('month', current_date)
                    group by
                        "primary-store-id",
                        "patient-id") t2
                on
                    t1."patient-id" = t2."patient-id"
                group by
                    "primary-store-id",
                    "behaviour-shift"
                    """

gen_shift = rs_db.get_df(gen_shift_q)

gen_shift_dist = pd.crosstab(index=gen_shift['store-id'],
                             columns=gen_shift['behaviour-shift'],
                             values=gen_shift['patient-count'],
                             aggfunc='sum', normalize='index')
# i = issue
gen_shift_dist_i = gen_shift_dist[gen_shift_dist['generic-shift'] <= gen_shift_dist['generic-shift'].quantile(0.05)]

store_ids = gen_shift_dist_i.index

for store_id in store_ids:
    store_name, store_emails = store_info_func(store_id)
    store_emails = ['shubham.gupta@zeno.health']
    gen_mail_body = f"""
    Hey {store_name} Store,
    Your store is in Top stores where generic substitution is lower for active consumer
    System average for active customer generic shift is  :  {gen_shift_dist['generic-shift'].quantile(0.5).round(4) * 100} %
    Your store performance : {gen_shift_dist_i.loc[store_id]['generic-shift'].round(4) * 100} %
    
    Your Weekly task to resolve this issues :
    
    > Focus on substitution for active customers 
    > Pitch Generic to customer whose generic affinity is lower
    """

    file_name = 'Substitution active consumer.xlsx'
    file_path = s3.write_df_to_excel(data={'Drugs': gen_shift_dist_i.loc[store_id]}, file_name=file_name)
    email.send_email_file(subject="Store Weekly Task 1 : Active Consumer substitution Issue",
                          mail_body=gen_mail_body,
                          to_emails=store_emails,
                          file_uris=[],
                          file_paths=[file_path])

#################################################################
############################ Sales  #############################
#################################################################

sale_tq = """select
                s."store-id",
                sum(case 
                    when s."created-at" >= date_trunc('month', current_date)
                    and s."created-at" <= current_date then s."revenue-value" else 0 end) "MTD-Sales",
                sum(case when s."created-at" >= dateadd('month', -1, date_trunc('month', current_date))
                    and s."created-at" <= dateadd('month', -1, current_date) then s."revenue-value" else 0 end) "LMTD-Sales",
                "MTD-Sales" - "LMTD-Sales" as "sales-diff",
                ("MTD-Sales" - "LMTD-Sales") / "LMTD-Sales" as "perc diff"
            from
                "prod2-generico".sales s
            left join "prod2-generico".stores s2 on
                s."store-id" = s2.id
            where
                s2."is-active" = 1
                and s2."franchisee-id" = 1
            group by
                s."store-id"
            having
                "sales-diff" < 0
                and "LMTD-Sales" != 0
                and min(s."created-at") < dateadd('month', -1, date_trunc('month', current_date))
            order by
                5
            limit 10"""

sale_t = rs_db.get_df(sale_tq)

store_ids = sale_t["store-id"].unique()

for store_id in store_ids:
    store_name, store_emails = store_info_func(store_id)
    store_emails = ['shubham.gupta@zeno.health']
    target = sale_t[sale_t["store-id"] == store_id]["sales-diff"].values[0]
    sales_mail_body = f"""
    Hey {store_name} Store,
    Your store is in Top stores in terms of sales de-growth 

    To exit from this phase you need to complete this sales target for today : {abs(target)}
    """

    email.send_email_file(subject="Store Daily Task 3 : Sales target for de-growing stores",
                          mail_body=sales_mail_body,
                          to_emails=store_emails,
                          file_uris=[],
                          file_paths=[])
