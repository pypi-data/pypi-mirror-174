from source.excel import Excel
from utils.utils import age
import json, dotenv, os, argparse
from termcolor import colored
from docxtpl import DocxTemplate
import os
from client.config import print_errors, BASEDIR, DATADIR
from termcolor import colored
from client.imm_api import imm_api_post

def getAppActions(pa):
    request = {"pa": pa.plain_dict}
    r = imm_api_post("pr/pickapp", request)
    if r.status_code == 200:
        return r.json()
    else:
        print_errors(r)
        return []


def getFormActions(pa, sp, dps, model):
    request = {
        "pa": pa.plain_dict,
        "sp": sp.plain_dict if sp else None,
        "dps": [dp.plain_dict for dp in dps],
        "model": model,
    }
    r = imm_api_post("pr/webform", request)
    if r.status_code == 200:
        return r.json()
    else:
        print_errors(r)
        return []


def login_prportal(rcic: str):
    # login
    path = os.path.abspath(os.path.join(os.path.expanduser("~"), ".immenv"))
    config = dotenv.dotenv_values(path)
    rcic_account = {
        "account": config.get(rcic + "_prportal_account"),
        "password": config.get(rcic + "_prportal_password"),
    }
    if not rcic_account["account"] or not rcic_account["password"]:
        print(
            colored(
                f"{rcic}'s prportal account and/or password is not existed. Check the .immenv file in your home directory and add your profile",
                "red",
            )
        )
        exit(1)

    r = imm_api_post("pr/login", rcic_account)
    if r.status_code == 200:
        return r.json()
    else:
        print_errors(r)
        return []


def output(args, actions):
    if args.to:
        with open(args.to, "w") as f:
            json.dump(actions, f, indent=3, default=str)
            print(colored(f"{args.to} is created", "green"))
    else:
        print(json.dumps(actions, indent=3, default=str))


def makeDocx(persons, docx_file):
    request = {"context": persons, "language": "English"}
    r = imm_api_post("pr/appendix", request)

    if r.status_code == 200:
        with open(docx_file, "wb") as f:
            f.write(r.content)
        print(colored(f"{docx_file} has been downloaded from web", "green"))
    else:
        print_errors(r)


def is_above_18(dp):
    person = dp.dict.get("personal")
    dob = person.get("dob")
    return True if age(dob) else False


def main():
    parser = argparse.ArgumentParser(
        description="Used for generating data for webform filling."
    )
    # input source excel files for pa, sp, and dp
    parser.add_argument(
        "-pa",
        "--principal_applicant",
        help="Input principal applicant's excel file name",
    )
    parser.add_argument("-sp", "--spouse", help="Input spouse's excel file name")
    parser.add_argument(
        "-dp",
        "--dependants",
        help="Input dependants' excel file names, can be multiple.",
        nargs="+",
    )
    # get which rcic
    parser.add_argument("-r", "--rcic", help="Input rcic's name")
    # generate data for filling all, or specific form
    parser.add_argument(
        "-f",
        "--forms",
        help="Specify generating which form. Exp: -f 5669 5562 0008 5406. Without -f, the app will generate all forms' data ",
        nargs="+",
    )
    # save to file
    parser.add_argument("-t", "--to", help="Input the output json file name")

    # make an additional appendix docx file including all information
    parser.add_argument("-a", "--appendix", help="Input the appendix file name")

    args = parser.parse_args()

    # get pa, sp, and dps object
    if args.principal_applicant:
        pa = Excel(args.principal_applicant)
    else:
        print(
            colored(
                "You didn't input principal applicant's excel file. Please use -pa excel.xlsl",
                "red",
            )
        )
        return

    if args.spouse:
        sp = Excel(args.spouse)
    else:
        sp = None

    dps = []
    if args.dependants:
        for excel in args.dependants:
            dps.append(Excel(excel))

    # make appendix doc file
    if args.appendix:
        dps_above_18 = [dp.plain_dict for dp in dps if is_above_18(dp)]
        sp = [sp.plain_dict] if sp else []
        makeDocx([pa.plain_dict, *sp, *dps_above_18], args.appendix)
        return
    # actions container
    actions = []
    # login
    if not args.rcic:
        print(
            colored(
                "You did not speficy using which rcic's portal. Please use -r rcic name",
                "red",
            )
        )
        return
    actions += login_prportal(args.rcic)
    # pick an existing application.
    actions += getAppActions(pa)

    # if args.form exists, then loop the form and generate them, else generate all forms
    if args.forms:
        a5406 = a5562 = a5669 = a0008 = []
        for form in args.forms:
            if form == "5406":
                a5406 = getFormActions(pa, sp, dps, "5406")
            elif form == "5562":
                a5562 = getFormActions(pa, sp, dps, "5562")
            elif form == "5669":
                a5669 = getFormActions(pa, sp, dps, "5669")
            elif form == "0008":
                a0008 = getFormActions(pa, sp, dps, "0008")
            else:
                print(
                    colored(
                        f"{form} is not a valid form number in '5562','5406','5669','0008'",
                        "red",
                    )
                )
                return
        actions += a5406 + a5562 + a5669 + a0008
        output(args, actions)
        return
    else:
        for form in ["5406", "5562", "5669", "0008"]:
            actions += getFormActions(pa, sp, dps, form)
        output(args, actions)
        return


if __name__ == "__main__":
    # pa = Excel("/Users/jacky/desktop/demo/all.xlsx")
    # sp = Excel("/Users/jacky/desktop/demo/all.xlsx")
    # dps = [pa, sp]
    # actions = []
    # actions += login_prportal("jacky")
    # # pick an existing application.
    # actions += getAppActions(pa)

    # for form in ["5406", "5562", "5669", "0008"]:
    #     actions += getFormActions(pa, sp, dps, form)
    # from pprint import pprint

    # dps_above_18 = [
    #     dp.plain_dict for dp in dps if is_above_18(dp)
    # ]  # doesn't check if it is above 18. Just for test
    # sp = [sp.plain_dict] if sp else []
    # makeDocx([pa.plain_dict, *sp, *dps_above_18], "aa.docx")

    main()
