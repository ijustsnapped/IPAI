# **Book Data Normalization and Blocking**

This project focuses on normalizing and performing a "blocking" process on book data from multiple datasets in order to detect duplicate records and perform accurate merges. The process is structured into three main stages: **Normalization**, **Blocking**, and **Data Merging**.

## **Features**

- **Data Normalization**: 
  - Normalizes fields such as ISBN, ASIN, book titles, and authors.
  - Converts titles and authors to lowercase, removes accents, extra spaces, and special characters.
  - Converts ISBN-10 to ISBN-13 to ensure consistent formatting.

- **Blocking and Data Comparison**: 
  - Uses a "blocking" technique to reduce the number of comparisons between records.
  - Compares authors using **Jaro-Winkler similarity** and book titles using **Jaccard similarity** to detect similar or duplicate books across datasets.

- **Data Merging**: 
  - Identifies and groups duplicate records across multiple datasets.
  - Exports the results to a CSV file, listing books found in more than one dataset along with the corresponding source datasets.

## **Code Structure**

The code is divided into several main sections:

1. **Normalization Functions**: These functions standardize data in columns like ISBN, ASIN, title, and author.
2. **Similarity and Comparison Functions**: These functions compare records using Jaro-Winkler for authors and Jaccard similarity for titles.
3. **Blocking Process**: Groups similar records together to avoid unnecessary comparisons.
4. **Exporting Results**: Outputs a final CSV containing merged data and matches found across multiple datasets.

## **How to Use**

### **Prerequisites**

- Python 3.x
- Required libraries:
  - `pandas`
  - `unidecode`
  - `isbnlib`
  - `jellyfish`
  - `re`

### **Steps**

1. Clone the repository or download the script.
2. Adjust the file paths for the datasets to your local system.
3. Run the script with:

   ```bash
   python blocking_code.py

The script will generate:

Normalized CSV files for each dataset.

A final CSV with records found across multiple datasets.

### **Costumization**
You can add additional columns for normalization or adjust similarity thresholds to fine-tune the comparison.

Modify the file paths for different datasets or add new ones as needed.

### **Example Data**
The code is designed to work with data from various sources, such as Amazon, Goodreads, BookCrossing, and more. Each of these datasets contains information about books, such as title, author, and unique identifiers like ISBN and ASIN. The script loads these datasets, performs normalization, and compares records to identify duplicate or similar books.
