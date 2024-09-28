import typer
from rich import print
from rich.prompt import Confirm

from db import Ad, Author
from db.config import config
from db.connection import start_db_connections, stop_db_connections
from db.models import Category, Delivery, ReasonClosing, Status
from db.session import session

app = typer.Typer(pretty_exceptions_enable=False)

statuses = [
    {'status_name': 'Open'},
    {'status_name': 'Close'},
    {'status_name': 'Reserved'},
]

categories = [
    {'category_name': 'Hoby'},
    {'category_name': 'Auto'},
    {'category_name': 'Realty'},
    {'category_name': 'Pets'},
    {'category_name': 'Work'},
    {'category_name': 'Clothes'},
    {'category_name': 'Food'},
    {'category_name': 'Child'},
    {'category_name': 'Electronics'},
]

delivery_list = [
    {'delivery_type': 'Terminal', 'price': 100},
    {'delivery_type': 'Courier', 'price': 200},
    {'delivery_type': 'Pickup_point', 'price': 50},
    {'delivery_type': 'Post_office', 'price': 70},
    {'delivery_type': 'Pickup', 'price': 0},
]

reasons = [
    {'reason_name': 'Sold Here'},
    {'reason_name': 'Sold Somewhere'},
    {'reason_name': 'Changed my mind'},
    {'reason_name': 'Other'},
]


@app.command()
def reset_db():
    print()
    confirmed = Confirm.ask(
        f":boom:Are you sure you want "
        f"to erase [red]all data[/red] in DB {config.URL}? :boom:"
    )
    if not confirmed:
        print('[green]OK[/green]')
        raise typer.Exit()

    start_db_connections()
    try:
        with session() as s:
            s.query(Author).delete()
            s.query(Ad).delete()
            s.query(Category).delete()
            s.query(Status).delete()
            s.query(Delivery).delete()
            s.query(ReasonClosing).delete()
            s.commit()

            for status in statuses:
                s.add(Status(**status))

            for category in categories:
                s.add(Category(**category))

            for delivery in delivery_list:
                s.add(Delivery(**delivery))

            for reason in reasons:
                s.add(ReasonClosing(**reason))

            s.commit()

        print('[green]Done[/green]')
    finally:
        stop_db_connections()


if __name__ == '__main__':
    app()
