name = "Alvyn"
year = 2020
link = "http://random.com"
# link = "random"

UpdateExpression = "SET"
ExpressionAtributeNames = {}
ExpressionAtributeValues = {}

if name is not None:
    UpdateExpression += " #name = :name"
    ExpressionAtributeNames |= {"#name": "name"}
    ExpressionAtributeValues |= {":name": name}
if year is not None:
    UpdateExpression += " #year = :year"
    ExpressionAtributeNames |= {"#year": "year"}
    ExpressionAtributeValues |= {":year": year}
if link is not None:
    UpdateExpression += " #link = :link"
    ExpressionAtributeNames |= {"#link": "link"}
    try:
        ExpressionAtributeValues |= {":link", link}
    except ValueError as e:
        print(e)
        ExpressionAtributeValues.update({":link": link})

print(f"{UpdateExpression=}\n{ExpressionAtributeNames=}\n{ExpressionAtributeValues=}")