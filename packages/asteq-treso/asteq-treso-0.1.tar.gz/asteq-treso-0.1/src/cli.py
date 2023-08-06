import click
import os
from functions import main_function,isUserIDRightFormat

sheet_name = 'account_operations'

@click.command()
@click.option('--set-user-id', '-u',show_default="",default=None, help="Will set the user id for Société Générale login")
@click.argument('filename',nargs=1)
def cli(set_user_id,filename):

    if os.getenv("USER_ID") == None :
        click.echo("USER_ID not found, please use '-u *your user_id*' flag to initiate it")

    #CLIENT
    if set_user_id != None:
        if isUserIDRightFormat(set_user_id):
            click.echo(f"Setting the USER_ID variable to {set_user_id}")
            os.environ["USER_ID"] = set_user_id
        else :
            return click.echo("Wrong format of user_id parameter : must be 8 digits (ex: 12345678)")
    
    if not(filename == "" or len(filename.split("."))<=1 or filename.split(".")[0]=="" or filename.split(".")[1]!='xlsx'):
        main_function(filename,sheet_name)
    else :
        click.echo(f"Incorrect filename : '{filename}', filename format must be like 'exemple.xlsx'")