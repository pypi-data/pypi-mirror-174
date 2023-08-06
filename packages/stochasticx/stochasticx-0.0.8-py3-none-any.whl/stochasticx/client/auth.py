import click
from stochasticx.auth.auth import Stochastic
from getpass import getpass

stochastic = Stochastic()

@click.command(name="login")
@click.option('--username', help='Username for login')
@click.option('--password', help='Password for login')
def login(username, password):
    if username is None:
        username = input("Enter your email: ")
    
    if password is None:
        password = getpass()
        
    stochastic.login(username, password)
        
    click.secho("[+] Login successfully", fg="green", bold=True)


@click.group(name="me")
def me():
    pass


@click.command(name="profile")
def profile():
    click.secho("\n[+] Collecting profile information", fg='blue', bold=True)
    profile_info = stochastic.get_profile()
    click.secho(profile_info, bold=True)
    

@click.command(name="company")
def company():
    company_info = stochastic.get_company()
    click.secho("\n[+] Collecting company information", fg='blue', bold=True)
    click.secho(company_info, bold=True)
    

@click.command(name="usage")
def usage():
    usage_info = stochastic.get_usage_quota()
    click.secho("\n[+] Collecting usage information", fg='blue', bold=True)
    click.secho(usage_info, bold=True)
    

me.add_command(profile)
me.add_command(company)
me.add_command(usage)