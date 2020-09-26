# Plagiarism Detector

A rudimentary plargiarism checker using cosine similarity and TF-IDF (term frequency–inverse document frequency). By essentially vectorizing commonly occuring words, we can measure how similar they are by calculating the cosine value of the two vectors. You can read more about cosine similarity [here](https://www.machinelearningplus.com/nlp/cosine-similarity/#:~:text=Cosine%20similarity%20is%20a%20metric,in%20a%20multi%2Ddimensional%20space.) The script is delivered as a web application using Python Flask. 

Flask is a microframework that allows Python developers to perform web development without importing any extra packages or any extra languages such as Java and NodeJS, making it very flexible and simple. 

After running the script, the plagiarism percentage will be shown on screen. The user can customize the percentage threshold; any percentage below the threshold will not detect plagiarism.

## Future improvements

We can improve the TF-IDF model by using sklearn's TfidfVectorizer package. We can also improve the UI by actually implementing a Javascript website rather than Flask's basic framework.



