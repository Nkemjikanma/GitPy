#!/usr/bin/env python3
import requests
from pprint import pprint
import json
import argparse
import os
import shutil

# TODO: Get my auth token from somewhere in pc
tokenFile = open('<token file url>')
token = tokenFile.read()
token = token.strip('\n')


class GitPy:
    def __init__(self):
        self.token = token
        self.API_URL = 'https://api.github.com'
        self.repo_path = '<local repo folder>'
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "token " + self.token
        }

        # using the argparse module to get arguments from terminal
        parser = argparse.ArgumentParser()
        parser.add_argument('--action', '-a', type=str, required=False, dest='action')
        parser.add_argument('--name', '-n', type=str, required=True, dest='name')
        parser.add_argument('--private', '-p', dest='is_private', action='store_true')
        # parser.add_argument('delete', '-d')
        args = parser.parse_args()
        self.repo_name = args.name
        self.is_private = args.is_private
        self.action = args.action

        if self.is_private:
            self.data = {
                "name": self.repo_name,
                'private': 'true'
            }
        else:
            self.data = {
                "name": self.repo_name,
                "private": "false"
            }

    # TODO: create create_repo method
    def create_repo(self):
        data = json.dumps(self.data)
        try:
            res = requests.post(self.API_URL + '/user/repos', data=data, headers=self.headers)
            print('created repo...\n now creating local dir')
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        try:
            os.chdir(self.repo_path)
            os.mkdir(self.repo_name)
            os.chdir(self.repo_path + self.repo_name)
            os.system('git init')
            os.system('git remote add origin <github url>/' + self.repo_name + '.git')
            os.system("echo '# " + self.repo_name + "'>> README.md")

            # I wrote my code in the default pycharm location and created the local repo in a different folder exclusive for git
            # If this doesn't apply to you, ignore the line below
            shutil.copyfile('<src folder where code is written>', self.repo_path + self.repo_name + '/' + self.repo_name +".py")
            print(self.repo_path + self.repo_name + self.repo_name + ".py")
            os.system("git add . && git commit -m 'Initial commit' && git push origin master")
        except FileExistsError as err:
            raise SystemExit(err)

    def delete_repo(self):
        repo_name = self.repo_name
        data = {
            "owner": "<username>",
            "repo": repo_name
        }
        data = json.dumps(data)
        try:
            res = requests.delete(
                self.API_URL+"/repos/<username>/" + repo_name,
                data=data,
                headers=self.headers
            )
            print('Succesfully deleted')
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

    def list_repo(self):
        try:
            res = requests.get(
                self.API_URL + '/user/repos',
                headers=self.headers
            )
            for repos in res.json():
                print(repos['name'])
            #pprint(res.json())
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)


if __name__ == "__main__":
    gitpy = GitPy()
    #gitpy.list_repo()
    if gitpy.action == 'delete':
        gitpy.delete_repo()
    elif gitpy.action == 'create':
        gitpy.create_repo()
    elif gitpy.action == 'list':
        gitpy.list_repo()

    if not gitpy.action:
        print('"-a create" to create repo || "-a delete" to delete repo || "-a list" to list repos')

