import datetime
import json

class Utils():

    @staticmethod
    def getDates(days):
        # get current date
        fromDateObject = datetime.datetime.now()
    
        #get days to date python lib object
        delta = datetime.timedelta(days=days)
        toDateObject = fromDateObject + delta

        # format as mm/dd/y
        fromDate = fromDateObject.strftime("%m/%d/%Y %H:%M")
        toDate = toDateObject.strftime("%m/%d/%Y %H:%M")

        return fromDate, toDate

    def get_today_str(format):
        today = datetime.datetime.now()
        today_str = today.strftime(format)
        return today_str

    def read_json(filepath):
        with open(filepath, 'r') as f:
            jsondata = json.loads(f.read())
            f.close()
        return jsondata

    def is_visitor_management_admin(admin_list, user_email):
        print(admin_list)
        print(user_email)
        if user_email in admin_list:
            return user_email
        return None

