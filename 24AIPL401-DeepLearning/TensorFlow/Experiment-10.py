import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, Model
from sklearn.model_selection import train_test_split

# 1. Load and preprocess data
df = pd.read_csv(r"D:/Work/Sairam/Subjects Handled/5. June-Dec 2026/Deep Learning Lab/Exp_10/New folder/DATA1/sales.csv")
df = df.dropna(subset=["customer_id", "product_id", "product_name",
                       "product_category", "quantity", "order_status"])
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["order_status"] = df["order_status"].astype(str).str.strip().str.lower()
df = df[(df["order_status"] == "completed") & (df["quantity"] > 0)].copy()

# 2. Create customer-product interactions
interactions = df.groupby(["customer_id", "product_id"], as_index=False).agg(
    quantity=("quantity", "sum"))
interactions["label"] = 1.0

customers = interactions["customer_id"].unique()
products = df.drop_duplicates("product_id").set_index("product_id")
user_map = {u: i for i, u in enumerate(customers)}
item_map = {p: i for i, p in enumerate(interactions["product_id"].unique())}
idx_to_item = {i: p for p, i in item_map.items()}

interactions["user_idx"] = interactions["customer_id"].map(user_map)
interactions["item_idx"] = interactions["product_id"].map(item_map)
num_users, num_items = len(user_map), len(item_map)

# 3. Generate negative samples
rng = np.random.default_rng(42)
purchased = interactions.groupby("user_idx")["item_idx"].apply(set).to_dict()
negative = [(u, i, 0.0) for u, items in purchased.items()
            for i in rng.choice([i for i in range(num_items) if i not in items],
                                size=min(4, len([i for i in range(num_items) if i not in items])),
                                replace=False)]

data = pd.concat([
    interactions[["user_idx", "item_idx", "label"]],
    pd.DataFrame(negative, columns=["user_idx", "item_idx", "label"])
], ignore_index=True)

# 4. Split data
train, val = train_test_split(data, test_size=0.2, random_state=42,
                              stratify=data["label"])

def make_inputs(d):
    return {"user_input": d["user_idx"].to_numpy(dtype=np.int32),
            "item_input": d["item_idx"].to_numpy(dtype=np.int32)}

X_train, y_train = make_inputs(train), train["label"].to_numpy(dtype=np.float32)
X_val, y_val = make_inputs(val), val["label"].to_numpy(dtype=np.float32)

# 5. Build recommendation model
user_input = layers.Input(shape=(1,), dtype="int32", name="user_input")
item_input = layers.Input(shape=(1,), dtype="int32", name="item_input")

u = layers.Flatten()(layers.Embedding(num_users, 32)(user_input))
i = layers.Flatten()(layers.Embedding(num_items, 32)(item_input))
x = layers.Concatenate()([u, i])
x = layers.Dense(64, activation="relu")(x)
x = layers.Dropout(0.2)(x)
x = layers.Dense(32, activation="relu")(x)
output = layers.Dense(1, activation="sigmoid")(x)

model = Model([user_input, item_input], output)
model.compile(optimizer="adam", loss="binary_crossentropy",
              metrics=[tf.keras.metrics.AUC(name="auc")])

# 6. Train model
model.fit(X_train, y_train, validation_data=(X_val, y_val),
          epochs=30, batch_size=64)

# 7. Recommend products
def recommend_products(customer_id, top_n=5):
    u = user_map[customer_id]
    candidates = [i for i in range(num_items)
                  if i not in purchased.get(u, set())]
    if not candidates:
        return pd.DataFrame()

    scores = model.predict({
        "user_input": np.full(len(candidates), u, dtype=np.int32),
        "item_input": np.array(candidates, dtype=np.int32)
    }, verbose=0).flatten()

    ranked = np.argsort(scores)[::-1][:top_n]
    return pd.DataFrame([{
        "product_id": idx_to_item[candidates[j]],
        "product_name": products.loc[idx_to_item[candidates[j]], "product_name"],
        "product_category": products.loc[idx_to_item[candidates[j]], "product_category"],
        "recommendation_score": round(float(scores[j]), 4)
    } for j in ranked])

# 8. Display recommendations
customer = customers[10]
print("Customer:", customer)
print(recommend_products(customer, 5).to_string(index=False))
