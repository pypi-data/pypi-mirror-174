import webbrowser
import pyfiglet
import sys
from requests import ConnectionError
from github import Github,UnknownObjectException,BadCredentialsException
from .config import TOKEN,TOKEN_INSERTED,PATH
import os
import clipboard


class GTExtract(Github):
    def __init__(self):
        super().__init__(TOKEN)

    def isValidUser(self, name):
        try:
            self.username = self.get_user(name)
            return True
        except UnknownObjectException as ex:
            if ex.status == 404:
                return False
        except BadCredentialsException as e:
            if e.status == 401:
                print("Please Enter the Valid Token\nRun The command Again to enter the Api Token")
                os.remove(f"{PATH}\\config.env")
                sys.exit(0)
        except ConnectionError :
            print("Please Connect to The Internet")
            sys.exit(0)

    @property
    def get_all_user_repos(self):
        return self.username.get_repos()

    def geturl(self, reponame, uname):
        repo = f"{uname}/{reponame}"
        return self.get_repo(repo).clone_url

HELP="""
Get The Github API token From github Setting
Paste the code

Using this Script you can Generate the Git url Which will automate the work of the Github.

For More Information Visit :
https://github.com/PrathameshDhande22/Giturlgetter
"""

def main():
    obj=GTExtract()
    if TOKEN_INSERTED is False:
        webbrowser.open(r"https://github.com/settings/tokens")
        try:
            token=input("Paste the Github Api Token : ")
        except KeyboardInterrupt as ki:
            print("Exiting...")
            sys.exit()
        except EOFError:
            print("Exiting..")
            sys.exit()
        with open(f"{PATH}\\config.env","w") as f:
            f.write(f"token={token}")
        print("Successfully entered the Token")
        menu(obj)
    else:
        menu(obj)
        
def menu(obj):
    lstrepo=[]
    no=[]
    text=pyfiglet.figlet_format("GITURLGETTER")
    print(text)
    try:
        while True:
                try:
                    choice=int(input('''\nEnter The following Commands 
                    1. Get git URL
                    2. Exit
                    3. Help\n
Enter Your Choice :'''))
                except KeyboardInterrupt as ki:
                    print("Exiting...")
                    sys.exit()
                except EOFError:
                    print("Exiting..")
                    sys.exit()
                if choice==1:
                    lstrepo.clear()
                    no.clear()
                    uname=input("Enter the Github Username :")
                    if obj.isValidUser(uname):
                        print("\nGetting Repos")
                        print("Repo No.\tRepo Name")
                        for index,repo in enumerate(obj.get_all_user_repos):
                            print(f"{index}\t{repo.name}")
                            lstrepo.append(repo.name)
                            no.append(index)
                        try:
                            ch=int(input("Enter the Repo Number :"))
                        except KeyboardInterrupt as ki:
                            print("Exiting...")
                            sys.exit()
                        except EOFError:
                            print("Exiting...")
                            sys.exit()
                        if ch in no:
                            r=lstrepo[no[ch]]
                            url=obj.geturl(r,uname)
                            print(url)
                            clipboard.copy(url)
                            print("Copied the Git URL")
                        else:
                            print("Enter the Valid Choice")
                            
                    else:
                        print("Username Not Found")

                elif choice==2:
                    print("Exiting..")
                    sys.exit(0)

                elif choice==3:
                    print(HELP)
    except ValueError:
        print("Enter the correct Choice")
        menu(obj)

