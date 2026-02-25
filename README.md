# 🏷 Live Auction System

## 📌 Overview
The **Live Auction System** is a web-based real-time auction platform that allows multiple participants to bid on items. It ensures progressive bidding, validates all bids, and declares the highest bidder at the end of the auction.

---

## 🎯 Objective
- Simulate a real-world auction experience
- Ensure each new bid is higher than the previous
- Track all bids and maintain bid history
- Provide a clean and user-friendly interface

---

## 🛠 Technologies Used
- **Python**  
- **Django Framework**  
- **HTML / CSS**  
- **SQLite** (Django default database)  
- **Visual Studio Code**

---

## ⚙ Features
- **Add Auction Items:** Admin can add new items with a starting price  
- **Progressive Bidding:** Ensures each bid is higher than the previous one  
- **Multiple Participants:** Allows multiple users to participate in an auction  
- **Bid History:** View all bids placed for an item  
- **Highest Bid Winner:** Declares the winner at the end of the auction  
- **Payment Confirmation:** Confirms payment for the winning bidder

---

## 🧠 Core Logic
1. Users can only place a bid if it is **higher than the current highest bid**  
2. Invalid bids are rejected with a message  
3. All valid bids are stored and continuously update the highest bid  
4. At auction end, the **highest bidder wins**, and payment is processed

---

## 📂 Project Structure
