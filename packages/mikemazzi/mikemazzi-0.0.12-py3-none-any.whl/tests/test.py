from mikemazzi import database as DB
from mikemazzi.functions import Functions as F
from mikemazzi import csvdata
import unittest
import pytest
import os
import csv

@pytest.mark.unittest
class UnitTests(unittest.TestCase):

    def test0(self):
        '''Test creazione database'''
        try:
            os.remove("users.db")
        except:
            print("Creazione database")
        
        try:
            userdb = DB.UserDB("users")
            userdb.testout()
            assert True
        except:
            assert False

    def test1(self):
        '''Test riempimento database'''
        try:
            userdb = DB.UserDB("users")
            userdb.add_user(["@mike","mail.test@mike.com","password1", "Michele", "male", 22])
            userdb.add_user(["@mazzi","mail.test@mazzi.it","password2", "Davide", "male", 22])
            userdb.add_user(["@user1","mail.test1@test.com","password3", "Test1", "other", 34])
            userdb.add_user(["@user2","mail.test2@test.com","password4", "Test2", "female", 50])
            assert True
        except:
            assert False

    def test2(self):
        '''Test riempimento database con errore'''
        try:
            userdb = DB.UserDB("users")
            userdb.add_user(["@username","mail.test@siu.com","sium", "Michele", "male", 22])
            userdb.add_user(["@username","mail.mazzi@siu.it","sssssssz!", "Davide", "male", 22])
            assert False
        except:
            assert True

    def test3(self):
        '''Test output informazioni'''
        userdb = DB.UserDB("users")
        try:
            userdb.add_user(["@mike123","mail.test@cazzi.com","sium", "Michele", "male", 22])
            userdb.add_user(["@mazzi123","mail.mazzi@sbura.it","sssssssz!", "Davide", "male", 22])
        except:
            print("già presenti")
        res = userdb.get_user_info("@mike")
        myres = {
            "username": "@mike", 
            "name": "Michele", 
            "gender": "male", 
            "age": 22
            }
        assert res == myres

    def test4(self):
        userdb = DB.UserDB("users")
        timeout = 10
        try:
            for x in range(0, timeout):
                try:
                    userdb.update_user("NAME", "Davide MAzzitelli", "@mazzi")
                    assert True
                except:
                    time.sleep(1)
                    pass
                finally:
                    break
            else:
                userdb.update_user("NAME", "Davide MAzzitelli", "@mazzi") 
                assert True
        except Exception as e:
            assert False
        #try:  
        #    assert True
        #except Exception as e:
        #    print(e)
        #    assert False
    #print(test1())


@pytest.mark.integtest
class IntegrationTests(unittest.TestCase):
    def test0(self):
        try:
            os.remove("users.db")
        except:
            print("Database doesn't exists")
        
        userdb = DB.UserDB("users")
        data = csvdata.RandomData()
        rm = data.stats[0]
        rf = data.stats[1]

        file = open('dataset.csv')
        type(file)
        csvreader = csv.reader(file)
        for row in csvreader:
            userdb.add_user(row)

        f1 = F(userdb)
        myResm = f1.male_stats()
        myResf = f1.female_stats()
        result = (myResm == rm) and (myResf == rf)

        assert result