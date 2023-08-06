class Functions():
    def __init__(self, db):
        self.Dbase = db

    def male_stats(self):
        db = self.Dbase
        dbRows = db.get_table()
        tot = 0
        count = 0
        avgAge = 0
        for u in dbRows:
            if u[2] == "male":
                count +=1
                avgAge += u[3]
            tot += 1
        percentage = (count * 100) / tot
        avgAge = avgAge/count

        res = {
            "male-count": count,
            "percentage": round(percentage,2),
            "average-age": round(avgAge,2)
        }
        return res
    
    def female_stats(self):
        db = self.Dbase
        dbRows = db.get_table()
        tot = 0
        count = 0
        avgAge = 0
        for u in dbRows:
            if u[2] == "female":
                count +=1
                avgAge += u[3]
            tot += 1
        percentage = (count * 100) / tot
        avgAge = avgAge/count

        res = {
            "female-count": count,
            "percentage": round(percentage,2),
            "average-age": round(avgAge, 2)
        }
        return res