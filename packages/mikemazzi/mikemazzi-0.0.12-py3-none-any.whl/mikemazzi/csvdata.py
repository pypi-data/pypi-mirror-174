import csv
import random
import string
import secrets



class RandomData():

    def __init__(self):
        self.stats = self.calculate_stats()


    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(secrets.choice(letters) for i in range(length))
        return result_str


    def create_dataset(self):
        genders = ["male", "female"]
        with open('dataset.csv', 'wt', encoding='utf-8') as f:
            type(f)
            writer = csv.writer(f)
            
            for x in range(1000):
                gender = secrets.choice(genders)
                system_random = random.SystemRandom()
                age = system_random.randint(13, 70)
                username = "@" + self.get_random_string(5) + str(x)
                email = self.get_random_string(5) + ".mail"
                password = self.get_random_string(8)
                name = self.get_random_string(5)

                data = [username, email, password, name, gender, age]
                try:
                    writer.writerow(data)
                except Exception:
                    print("username not unique")


            # close the file
            f.close()

    def calculate_stats(self):
        self.create_dataset()
        with open('dataset.csv', 'rt', encoding='utf-8') as file:
            type(file)
            csvreader = csv.reader(file)
            count_male = 0
            count_female = 0
            tot = 0
            avgAge_male = 0
            avgAge_female = 0
            for row in csvreader:
                if row[4] == 'male':
                    count_male += 1
                    avgAge_male += int(row[5])
                else:
                    count_female += 1
                    avgAge_female += int(row[5])
                tot += 1
            
            avgAge_female = avgAge_female/count_female
            avgAge_male = avgAge_male/count_male

            percentage_female = (count_female * 100) / tot
            percentage_male = (count_male * 100) / tot

            res_female = {
                    "female-count": count_female,
                    "percentage": round(percentage_female,2),
                    "average-age": round(avgAge_female,2)
                }
            
            res_male = {
                    "male-count": count_male,
                    "percentage": round(percentage_male,2),
                    "average-age": round(avgAge_male,2)
                }

            file.close()
        return [res_male, res_female]