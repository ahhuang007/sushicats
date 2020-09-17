from flask import Flask, render_template, request, session
import pandas as pd
import gower
import numpy as np
app = Flask(__name__)
app.secret_key = "Armadyl42"
li = []
ids = []
cate = [0]
cate.extend([1]*43)
cate.extend([0,1,0,0,0,0])
weights = [2]+(43*[1]) + (6*[5])
#df = pd.read_csv("Data/p_compiled_data.csv") #large image base, not able to use
df = pd.read_csv("Data/partial_data.csv") #most we can have for free
#df = pd.read_csv("Data/processed_data.csv") #small dataset
lnum = 79999 #205643 for comp, 79999 for part, 11604 for proc

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        #request was a POST
        session["li"] = []
        session["ids"] = []
        
        num = np.random.randint(0,lnum)
        src = df["Src"][num]
        size = eval(df["Size"][num])
        
        he = size[1] * 20
        wi = size[0] * 20
        
        #ids.append(num)
        session["ids"].append(num)
        session.modified = True
        return render_template('question.html', source = src, he = he, wi = wi)
    


@app.route('/about', methods = ['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/question', methods = ['GET','POST'])
def question():
    if request.method == 'POST':
        selected = request.form.getlist('like')[0]
        #li.append(selected)
        session["li"].append(selected)
        session.modified = True
        ny = len([i for i in session['li'] if i == "yes"])
        print("question")
        print(session["li"])
        if ny >= 5 and len(session['li']) >= 10:
            picks = get_results(session['li'], session['ids'])
            #Witness some solid code here
            start = "https://www.art.com"
            return render_template('result.html',
                                   im0 = df["Src"][picks[0]],
                                   wi0 = eval(df["Size"][picks[0]])[0] * 20,
                                   he0 = eval(df["Size"][picks[0]])[1] * 20,
                                   ti0 = df["Title"][picks[0]],
                                   li0 = start + df["Link"][picks[0]] + "/",
                                   im1 = df["Src"][picks[1]],
                                   wi1 = eval(df["Size"][picks[1]])[0] * 20,
                                   he1 = eval(df["Size"][picks[1]])[1] * 20,
                                   ti1 = df["Title"][picks[1]],
                                   li1 = start + df["Link"][picks[1]] + "/",
                                   im2 = df["Src"][picks[2]],
                                   wi2 = eval(df["Size"][picks[2]])[0] * 20,
                                   he2 = eval(df["Size"][picks[2]])[1] * 20,
                                   ti2 = df["Title"][picks[2]],
                                   li2 = start + df["Link"][picks[2]] + "/",
                                   im3 = df["Src"][picks[3]],
                                   wi3 = eval(df["Size"][picks[3]])[0] * 20,
                                   he3 = eval(df["Size"][picks[3]])[1] * 20,
                                   ti3 = df["Title"][picks[3]],
                                   li3 = start + df["Link"][picks[3]] + "/",
                                   im4 = df["Src"][picks[4]],
                                   wi4 = eval(df["Size"][picks[4]])[0] * 20,
                                   he4 = eval(df["Size"][picks[4]])[1] * 20,
                                   ti4 = df["Title"][picks[4]],
                                   li4 = start + df["Link"][picks[4]] + "/")
        else:
            
            num = np.random.randint(0,lnum)
            src = df["Src"][num]
            size = eval(df["Size"][num])
            he = size[1] * 20
            wi = size[0] * 20
            #ids.append(num)
            session["ids"].append(num)
            session.modified = True
            return render_template('question.html', source = src, he = he, wi = wi)

def get_results(li, ids):
    cdf = df.copy()
    cdf = cdf.drop([df.columns[0]], axis = 1)

    cdf = cdf.drop(['Title','Size','Link','Filename','Src'], axis = 1)
    yeses = []
    nos = []
    print(ids)
    print(li)
    for i in range(len(ids)):
        if li[i] == "no":
            #get top n for el, remove
            nos.append(ids[i])
        elif li[i] == "eh":
            #remove el
            cdf = cdf.drop([ids[i]])
        else:
            yeses.append(ids[i])
    print(yeses)
    print(nos)
    if nos:
        minidf = cdf[cdf.index.isin(nos)]
        cdf = cdf.drop(nos)
        worst = gower.gower_topn(minidf, cdf, n = 9 * len(nos), 
                             weight=np.array(weights), cat_features=cate)
        for el in list(worst['index']):
            if el in cdf.index:
                cdf = cdf.drop([el])
        #cdf = cdf.drop(list(worst['index']))
    rows = cdf[cdf.index.isin(yeses)]
    cdf = cdf.drop(yeses)
    best = gower.gower_topn(rows, cdf, n = 5, weight = np.array(weights), 
                            cat_features = cate)
    recs = list(best['index'])
    
    return recs

@app.route('/reset', methods = ['GET', 'POST'])
def reset():
    if request.method == 'POST':
        #li.clear()
        #ids.clear()
        session["li"] = []
        session["ids"] = []
        print("reset")
        print(session["li"])
        num = np.random.randint(0,lnum)
        src = df["Src"][num]
        size = eval(df["Size"][num])
        he = size[1] * 20
        wi = size[0] * 20
        #ids.append(num)
        session["ids"].append(num)
        session.modified = True
        return render_template('question.html', source = src, he = he, wi = wi)

if __name__ == '__main__':
    app.run(port=33507, debug = True)
