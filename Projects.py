import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 500)

df = pd.read_csv("dataset.csv")

"""
"Make" - The company that manufactures the vehicle.
"Model" - The vehicle's model.
"Vehicle Class" - Vehicle class by utility, capacity, and weight.
"Engine Size(L)" - The engine's displacement in liters.
"Cylinders" - The number of cylinders.
"Transmission" - The transmission type: A = Automatic, AM = Automatic Manual, AS = Automatic with select shift, AV = Continuously variable, M = Manual, 3 - 10 = the number of gears.
"Fuel Type" - The fuel type: X = Regular gasoline, Z = Premium gasoline, D = Diesel, E = Ethanol (E85), N = natural gas.
"Fuel Consumption Comb (L/100 km)" - Combined city/highway (55%/45%) fuel consumption in liters per 100 km (L/100 km).
"CO2 Emissions(g/km)" - The tailpipe carbon dioxide emissions in grams per kilometer for combined city and highway driving.
"""

def check_df(dataframe, head = 5):
    print("-----------------------Shape-----------------------")
    print(dataframe.shape)
    print("-----------------------Dtypes-----------------------")
    print(dataframe.dtypes)
    print("-----------------------Head-----------------------")
    print(dataframe.head(head))
    print("-----------------------Tail-----------------------")
    print(dataframe.tail(head))
    print("-----------------------NA-----------------------")
    print(dataframe.isnull().sum())
    print("-----------------------Quantiles-----------------------")
    print(dataframe.describe())

check_df(df)

def grab_col_names(dataframe, cat_th = 10, car_th = 20):
    cat_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"]]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and dataframe[col].dtypes in ["int", "float"]]
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and str(dataframe[col].dtypes) in ["category", "object"]]
    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]
    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes in ["int", "float"]]
    num_cols = [col for col in num_cols if col not in cat_cols]
    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f"cat_cols: {len(cat_cols)}")
    print(f"num_cols: {len(num_cols)}")
    print(f"cat_but_car: {len(cat_but_car)}")
    print(f"num_but_cat: {len(num_but_cat)}")
    return cat_cols, num_cols, cat_but_car

cat_cols, num_cols, cat_but_car = grab_col_names(df)

def cat_summary(dataframe, col_name, plot = False):
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
    print("------------------------------------------------------------------")
    if plot:
        sns.countplot(x = dataframe[col_name], data = dataframe)
        plt.show()

for col in cat_cols:
    cat_summary(df, col, plot = True)

def num_summary(dataframe, numerical_col, plot = False):
    print(dataframe[numerical_col].describe().T)
    if plot:
        dataframe[numerical_col].hist()
        plt.title(numerical_col)
        plt.xlabel(numerical_col)
        plt.show(block = False)

for col in num_cols:
    num_summary(df, col, plot = True)


#What is the median engine size in liters?

df["Engine Size(L)"].median()

#What is the average fuel consumption for regular gasoline (Fuel Type = X), premium gasoline (Z), ethanol (E), and diesel (D)?

df.groupby("Fuel Type").agg({"Fuel Consumption Comb (L/100 km)": "mean"})

#What is the correlation between fuel consumption and CO2 emissions?

df["Fuel Consumption Comb (L/100 km)"].corr(df["CO2 Emissions(g/km)"])

#Which vehicle class has lower average CO2 emissions, 'SUV - SMALL' or 'MID-SIZE'?

suv_small = df[df["Vehicle Class"] == "SUV - SMALL"]
mid_size = df[df["Vehicle Class"] == "MID-SIZE"]

suv_small_mean = suv_small["CO2 Emissions(g/km)"].mean()
mid_size_mean = mid_size["CO2 Emissions(g/km)"].mean()

if suv_small_mean > mid_size_mean:
    print("SUV - SMALL Vehicle Class is bigger")
else:
    print("MID-SIZE Vehicle Class is bigger")

#What are the average CO2 emissions for all vehicles? For vehicles with an engine size of 2.0 liters or smaller?

df["CO2 Emissions(g/km)"].mean()

engine_size_2 = df[df["Engine Size(L)"] == 2]

engine_size_2["CO2 Emissions(g/km)"].mean()

#Any other insights you found during your analysis?

#Scatter plot of Fuel Consumption vs CO2 Emissions

sns.scatterplot(x = "Fuel Consumption Comb (L/100 km)", y = "CO2 Emissions(g/km)", data = df)
plt.xlabel("Fuel Consumption Comb (L/100 km)")
plt.ylabel("CO2 Emissions(g/km)")
plt.title("Fuel Consumption vs CO2 Emissions")
plt.show()

#*Bu kod, yakıt tüketimi (Fuel Consumption Comb) ve CO2 emisyonu (CO2 Emissions) arasındaki ilişkiyi görselleştirir. Her bir aracın yakıt tüketimi ve CO2 emisyonu değerleri arasında bir nokta yer alır. Bu şekilde, yakıt tüketimi ile CO2 emisyonu arasındaki genel ilişkiyi gözlemleyebilirsiniz.

#Box plot of Engine Size vs CO2 Emissions

sns.boxplot(x = "Engine Size(L)", y = "CO2 Emissions(g/km)", data = df)
plt.xlabel("Engine Size(L)")
plt.ylabel("CO2 Emissions(g/km)")
plt.title("Engine Size vs CO2 Emissions")
plt.show()

#*Bu kod, motor büyüklüğü (Engine Size) ve CO2 emisyonu (CO2 Emissions) arasındaki ilişkiyi kutu grafiği ile görselleştirir. Bu şekilde, farklı motor boyutlarına sahip araçların CO2 emisyonu dağılımını karşılaştırabilirsiniz.

#Bar plot of Cylinders vs CO2 Emissions

sns.barplot(x = "Cylinders", y = "CO2 Emissions(g/km)", data = df)
plt.xlabel("Cylinders")
plt.ylabel("CO2 Emissions(g/km)")
plt.title("Cylinders vs CO2 Emissions")
plt.show()

#*Bu kod, silindir sayısı (Cylinders) ve CO2 emisyonu (CO2 Emissions) arasındaki ilişkiyi bar grafiği ile görselleştirir. Bu şekilde, farklı silindir sayısına sahip araçların ortalama CO2 emisyonunu karşılaştırabilirsiniz.

#Box plot of Fuel Type vs CO2 Emissions

sns.boxplot(x = "Fuel Type", y = "CO2 Emissions(g/km)", data = df)
plt.xlabel("Fuel Type")
plt.ylabel("CO2 Emissions")
plt.title("Fuel Type vs CO2 Emissions")
plt.show()

#*Bu kod, yakıt türü (Fuel Type) ve CO2 emisyonu (CO2 Emissions) arasındaki ilişkiyi kutu grafiği ile görselleştir

#Histogram of Fuel Consumption

sns.histplot(x = "Fuel Consumption Comb (L/100 km)", data = df)
plt.xlabel("Fuel Consumption Comb (L/100 km)")
plt.ylabel("Frequency")
plt.title("Fuel Consumption Distribution")
plt.show()

#*Bu kod, yakıt tüketimi (Fuel Consumption Comb) dağılımını histogram olarak görselleştirir. Bu şekilde, yakıt tüketiminin hangi değerlerde yoğunlaştığını ve genel dağılımını görebilirsiniz.

#Bar plot of Top 10 Most Common Car Makes

top_10_makes = df["Make"].value_counts().head(10)

sns.barplot(x = top_10_makes.index, y = top_10_makes.values)
plt.xlabel("Car Make")
plt.ylabel("Count")
plt.title("Top 10 Most Common Car Makes")
plt.xticks(rotation = 75)
plt.show()

#*Bu kod, en yaygın araç markalarını bar grafiği olarak görselleştirir. Bu şekilde, hangi araç markalarının veri setinizde en yaygın olduğunu görebilirsiniz.

#Violin plot of Fuel Consumption by Vehicle Class

sns.violinplot(x = "Fuel Consumption Comb (L/100 km)", y = "Vehicle Class", data = df)
plt.xlabel("Fuel Consumption Comb (L/100 km)")
plt.ylabel("Vehicle Class")
plt.title("Fuel Consumption by Vehicle Class")
plt.show()

#*Bu kod, araç sınıflarına göre yakıt tüketimi dağılımını keman grafiği (violin plot) olarak görselleştirir. Bu şekilde, farklı araç sınıflarının yakıt tüketimi dağılımlarını ve merkezi eğilimlerini karşılaştırabilirsiniz.
