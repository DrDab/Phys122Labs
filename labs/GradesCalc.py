def getExamScore(mt1, mt2, final):
    mt1s = mt1 / 100.0
    mt2s = mt2 / 100.0
    finals = final / 100.0
    g1 = (mt1s + mt2s + finals) * .6 / 3
    g2 = (max(mt1s, mt2s) * .2) + (finals * .4)
    if g1 > g2:
        print("Using method 1 of exam scaling")
        return g1
    else:
        print("Using method 2 of exam scaling")
        return g2

def percentToGPA(percent):
    if percent >= .92:
        return 4.0
    if percent >= .904 and percent < .92:
        return 3.9
    if percent >= .888 and percent < .904:
        return 3.8
    if percent >= .872 and percent < .888:
        return 3.7
    if percent >= .856 and percent < .872:
        return 3.6
    if percent >= .84 and percent < .856:
        return 3.5
    if percent >= .824 and percent < .84:
        return 3.4
    if percent >= .808 and percent < .824:
        return 3.3
    if percent >= .792 and percent < .808:
        return 3.2
    if percent >= .776 and percent < .792:
        return 3.1
    if percent >= .76 and percent < .776:
        return 3.0
    return -1

print("Enter your assignment score")
ass = float(input())
print("Enter your midterm 1")
mt1 = float(input())
print("Enter your midterm 2")
mt2 = float(input())
print("Enter your final")
final = float(input())
print("-------------")
print()
examScore = getExamScore(mt1, mt2, final)
assScore = ass * .4
assScoreS = assScore / 100.0
combScore = examScore + assScoreS
print("Combined assignment score: %.1f%% of 40.0%% possible" % (assScore))
print("Combined exam score: %.1f%% of 60.0%% possible" % (examScore * 100.0))
print("Combined score: %.1f%%" % (combScore * 100.0))
print("GPA: %.1f" % percentToGPA(combScore))
