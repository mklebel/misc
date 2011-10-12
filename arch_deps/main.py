#!/usr/bin/python2.7

from pyparsing import *
import os, sys, MySQLdb, shlex, subprocess

def get_pkg_id(conn, cursor, pkg_name):
    sql = "SELECT id FROM package WHERE name = %s"   
    cursor.execute(sql, pkg_name)
    row = cursor.fetchone()
    if row == None:
        return None
    else:
        return row[0]
  
def insert_pkg(conn, cursor, pkg_name):
    if get_pkg_id(conn, cursor, pkg_name) == None:
        sql = "INSERT INTO package (name) VALUES(%s)"
        cursor.execute(sql, pkg_name)
        conn.commit()
        return cursor.lastrowid
    else:
        return get_pkg_id(conn, cursor, pkg_name)  

def insert_pkg_dep(conn, cursor, pkg_id, pkg_dep_id):
    sql = "INSERT INTO package_dependency (package_id, package_dep_id) VALUES(%s, %s)"
    cursor.execute(sql, (pkg_id, pkg_dep_id))
    conn.commit()

## mysql shtuff ##
conn = MySQLdb.connect(host = "localhost", user = "", passwd = "", db = "arch_deps")
cursor = conn.cursor()

## statics ##
abs_path = '/var/abs/'
repo_list = os.listdir(abs_path)

## pyparsing ##
ident = Word(alphas + " " + alphas)
pacman = ident + Suppress(":") + empty + restOfLine


## loop through the /var/abs dirs
for repo in repo_list:
    if repo <> 'local' and repo <> 'README':
        ## get list of pkgs ##
        pkg_list = os.listdir(abs_path+repo)

        for pkg_name in pkg_list:                        
            try:
                ## grab pacman -Si output and process with pyparser ##
                pacman_output = subprocess.check_output(["pacman", "-Si", pkg_name])
                pacman_output = pacman.searchString(pacman_output)
                
                ## insert pkgname into the DB and return unique_id ##
                pkg_id = insert_pkg(conn, cursor, pkg_name)

                pkg_info = {}

                for x in pacman_output:
                    # rstrip() because I can't figure out how to strip trailing whitespace with pyparsing
                    pkg_info[x[0].rstrip()] = x[1]
                
                ## split deps into list ##
                pkg_info['Depends On'] = pkg_info['Depends On'].split()

                for pkg_name in pkg_info['Depends On']:
                    ## insert or get dep pkg id ##
                    pkg_dep_id = insert_pkg(conn, cursor, pkg_name)

                    ## insert pkg dep ##
                    insert_pkg_dep(conn, cursor, pkg_id, pkg_dep_id)            
            except:
                print pkg_name+" :: Skipped :: "
