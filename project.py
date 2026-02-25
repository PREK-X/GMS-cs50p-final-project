from tabulate import tabulate
from pyfiglet import figlet_format
from datetime import date
from datetime import timedelta
from rich.console import Console
from rich.panel import Panel
from rich import box

import secrets
import sys
import csv
import os


def main():

    console = Console()

    big_text = figlet_format("GYM MANAGEMENT SYSTEM")

    panel = Panel(
        f"[red]{big_text}[/red]",
        title="Welcome to",
        box=box.HEAVY,
        title_align="center",
        style="bold",
        border_style="bold",
        width=90,
    )

    console.print(panel)

    while True:

        print(main_menu())
        try:

            i = int(input("Select Option: "))

        except ValueError:

            print("Wrong Input!")
            continue

        match i:
            case 1:
                print(new_member())
            case 2:
                print(show_all_members())
            case 3:
                search_member()
            case 4:
                print(memberships())
            case 5:
                payment_status()
            case 6:
                print(delete_member())
            case 7:
                print(edit_member())
            case 8:
                sys.exit()
            case _:
                print("Wrong Input!")
                continue


def main_menu():

    return """
 1. create new member
 2. show all registered members
 3. search existing member
 4. memberships available
 5. payment status
 6. delete member data
 7. edit member data
 8. exit
    """


def new_member():

    monthly_membership_fee = {
        "basic": 3000,
        "premium": 5000,
        "ultimate": 7000,
        "mma": 3000,
    }

    halfyear_membership_fee = {
        "basic": 15000,
        "premium": 25000,
        "ultimate": 35000,
        "mma": 15000,
    }

    yearly_membership_fee = {
        "basic": 26000,
        "premium": 45000,
        "ultimate": 65000,
        "mma": 26000,
    }

    file_path = "gym.csv"
    id = secrets.randbelow(1000)
    today = date.today()
    name = input("What's your name? ").lower()

    try:

        age = int(input("What's your age? "))

    except ValueError:

        return "Wrong Age Input!"

    print(memberships(), end="\n")
    duration = input("Membership duration(e.g: monthly/6 months/yearly): ").lower()

    if duration not in ["monthly", "6 months", "yearly"]:
        return "Wrong duration input! Select from suggested options"
    membership = input("Select your preffered membership(plan): ").lower()
    if membership not in ["basic", "premium", "ultimate", "mma"]:
        return "Wrong membership input! Select from suggested options"

    if duration == "monthly":
        payment_fee = monthly_membership_fee[membership]
        time = timedelta(days=30)
    elif duration == "6 months":
        payment_fee = halfyear_membership_fee[membership]
        time = timedelta(days=182)
    else:
        payment_fee = yearly_membership_fee[membership]
        time = timedelta(days=365)

    renew_date = today + time

    file_exist = os.path.exists(file_path)

    with open(file_path, "a+", newline="") as csvfile:
        fieldnames = [
            "id",
            "name",
            "age",
            "date",
            "membership",
            "duration",
            "payment fee",
            "renew date",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exist:
            writer.writeheader()

        writer.writerow(
            {
                "id": id,
                "name": name,
                "age": age,
                "date": today,
                "membership": membership,
                "duration": duration,
                "payment fee": payment_fee,
                "renew date": renew_date,
            }
        )

        return "Member Created Successfully!"


def show_all_members():

    table = []
    headers = ["id", "name", "age", "date", "membership", "duration", "payment fee"]

    try:
        with open("gym.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                table.append(
                    [
                        row["id"],
                        row["name"],
                        row["age"],
                        row["date"],
                        row["membership"],
                        row["duration"],
                        row["payment fee"],
                    ]
                )

    except FileNotFoundError:
        return "No member exist"

    return tabulate(table, headers, tablefmt="rounded_grid")


def search_member():

    all_ids = []
    table = []
    headers = ["id", "name", "age", "date", "membership", "duration", "payment fee"]
    try:
        with open("gym.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            id = input("Enter the member's id: ")

            for row in reader:

                all_ids.append(row["id"])

                if row["id"] == id:
                    table.append(
                        [
                            row["id"],
                            row["name"],
                            row["age"],
                            row["date"],
                            row["membership"],
                            row["duration"],
                            row["payment fee"],
                        ]
                    )
                    print(tabulate(table, headers, tablefmt="rounded_grid"))

        if id not in all_ids:
            print("Wrong ID!")

    except FileNotFoundError:
        print("No Member Exist")



def memberships():

    return tabulate(
        [
            ["Plan", "Access", "Monthly(Rs)", "6 Months(Rs)", "Yearly(Rs)"],
            ["Basic", "GYM", 3000, 15000, 26000],
            ["premium", "GYM + Cardio", 5000, 25000, 45000],
            ["Ultimate", "GYM + Cardio + MMA + Trainer", 7000, 35000, 65000],
            ["MMA", "MMA + Trainer", 3000, 15000, 26000],
        ],
        headers="firstrow",
        tablefmt="rounded_grid",
    )


def payment_status():

    all_ids = []
    table = []
    headers = [
        "id",
        "name",
        "date",
        "membership",
        "duration",
        "membership fee",
        "renew date",
    ]
    try:
        with open("gym.csv", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            id = input("Enter the member's id: ")

            for row in reader:

                all_ids.append(row["id"])

                if row["id"] == id:
                    table.append(
                        [
                            row["id"],
                            row["name"],
                            row["date"],
                            row["membership"],
                            row["duration"],
                            row["payment fee"],
                            row["renew date"],
                        ]
                    )
                    print(tabulate(table, headers, tablefmt="rounded_grid"))

        if id not in all_ids:
            print("\nWrong id!")
    except FileNotFoundError:
        print("No Member Exist")


def delete_member():

    file_path = "gym.csv"
    all_members = []
    member_list = []

    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            id = input("Enter the id of the user you want to delete: ")

            for row in reader:

                all_members.append(row["id"])

                if row["id"] != id:
                    member_list.append(
                        {
                            "id": row["id"],
                            "name": row["name"],
                            "age": row["age"],
                            "date": row["date"],
                            "membership": row["membership"],
                            "duration": row["duration"],
                            "payment fee": row["payment fee"],
                            "renew date": row["renew date"],
                        }
                    )
                    
    except FileNotFoundError:
        return "No Member Exist"


    with open(file_path, "w", newline="") as csvfile:

        fieldnames = [
            "id",
            "name",
            "age",
            "date",
            "membership",
            "duration",
            "payment fee",
            "renew date",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(member_list)

    if id not in all_members:
        return "\nWrong id!"
    else:
        return "Member deleted successfully!"


def edit_member():

    file_path = "gym.csv"
    all_members_info = []
    all_ids = []
    today = date.today()
    time_days = 0

    monthly_membership_fee = {
        "basic": 3000,
        "premium": 5000,
        "ultimate": 7000,
        "mma": 3000,
    }

    halfyear_membership_fee = {
        "basic": 15000,
        "premium": 25000,
        "ultimate": 35000,
        "mma": 15000,
    }

    yearly_membership_fee = {
        "basic": 26000,
        "premium": 45000,
        "ultimate": 65000,
        "mma": 26000,
    }

    gym_memberships = [
        monthly_membership_fee,
        halfyear_membership_fee,
        yearly_membership_fee,
    ]

    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

    except FileNotFoundError:
        return "No Member Exist"


    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        choice = int(
            input(
                "Do you want to edit member's info(name/age) or membership?(select '1' or '2'): "
            )
        )

        if choice not in [1, 2]:

            return "\nWrong Input! Select from suggested options."

        id = input("Enter ID of the member you want to edit: ")

        for row in reader:

            all_ids.append(row["id"])

            if row["id"] != id:
                all_members_info.append(
                    {
                        "id": row["id"],
                        "name": row["name"],
                        "age": row["age"],
                        "date": row["date"],
                        "membership": row["membership"],
                        "duration": row["duration"],
                        "payment fee": row["payment fee"],
                        "renew date": row["renew date"],
                    }
                )

            if row["id"] == id:

                if choice == 1:

                    name = input("Enter updated name: ").lower()

                    try:

                        age = int(input("Enter age: "))

                    except ValueError:

                        return "\nWrong Age Input"

                    all_members_info.append(
                        {
                            "id": row["id"],
                            "name": name,
                            "age": age,
                            "date": row["date"],
                            "membership": row["membership"],
                            "duration": row["duration"],
                            "payment fee": row["payment fee"],
                            "renew date": row["renew date"],
                        }
                    )

                elif choice == 2:

                    new_membership = input(
                        "Enter the new membership(basic/premium/ultimate/mma): "
                    ).lower()

                    if new_membership not in ["basic", "premium", "ultimate", "mma"]:
                        return "Wrong membership! select from suggested options."

                    duration = input(
                        "Enter membership duration(monthly/6 months/yearly): "
                    )

                    if duration not in ["monthly", "6 months", "yearly"]:
                        return "Wrong duration! select from suggested options."

                    if duration == "monthly":
                        payment_fee = gym_memberships[0][new_membership]
                        time_days = timedelta(days=30)
                    elif duration == "6 months":
                        payment_fee = gym_memberships[1][new_membership]
                        time_days = timedelta(days=182)
                    elif duration == "yearly":
                        payment_fee = gym_memberships[2][new_membership]
                        time_days = timedelta(days=365)

                    renew_date = time_days + today

                    all_members_info.append(
                        {
                            "id": row["id"],
                            "name": row["name"],
                            "age": row["age"],
                            "date": today,
                            "membership": new_membership,
                            "duration": duration,
                            "payment fee": payment_fee,
                            "renew date": renew_date,
                        }
                    )

    if id not in all_ids:
        return "Wrong ID! Enter a valid user ID."

    with open(file_path, "w", newline="") as csvfile:
        fieldnames = [
            "id",
            "name",
            "age",
            "date",
            "membership",
            "duration",
            "payment fee",
            "renew date",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_members_info)

        return "Changes Made Successfully!"


if __name__ == "__main__":
    main()
