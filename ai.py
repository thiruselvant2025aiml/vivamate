import os
import random
from dotenv import load_dotenv

load_dotenv()

AI_MODE = os.getenv("AI_MODE", "demo")


QUESTION_BANK = {

    "dsa": {
        "easy": [
            "What is a data structure?",
            "What is an array?",
            "What is a stack?",
            "What is a queue?",
            "What is a linked list?"
        ],

        "medium": [
            "What is the difference between an array and a linked list?",
            "What is the difference between stack and queue?",
            "What is a circular queue?",
            "What is a doubly linked list?",
            "What is the time complexity of binary search?"
        ],

        "hard": [
            "Explain binary search tree and its operations.",
            "What is tree traversal? Explain its types.",
            "What is the difference between BFS and DFS?",
            "Explain recursion with an example.",
            "What is dynamic programming?"
        ]
    },


    "python": {
        "easy": [
            "What is Python?",
            "What are variables in Python?",
            "What is a list in Python?",
            "What is a tuple in Python?",
            "What is a function?"
        ],

        "medium": [
            "What is the difference between a list and a tuple?",
            "What is a dictionary in Python?",
            "What are Python modules?",
            "What is exception handling?",
            "What is list comprehension?"
        ],

        "hard": [
            "Explain object-oriented programming in Python.",
            "What are decorators in Python?",
            "What is a lambda function?",
            "Explain inheritance in Python.",
            "What is the difference between shallow copy and deep copy?"
        ]
    },


    "java": {
        "easy": [
            "What is Java?",
            "What is a class?",
            "What is an object?",
            "What is inheritance?",
            "What is polymorphism?"
        ],

        "medium": [
            "What is method overloading?",
            "What is method overriding?",
            "What is encapsulation?",
            "What is abstraction?",
            "What is an interface?"
        ],

        "hard": [
            "Explain runtime polymorphism in Java.",
            "What is the difference between abstract class and interface?",
            "Explain exception handling in Java.",
            "What is multithreading?",
            "Explain the Java Virtual Machine."
        ]
    },


    "c++": {
        "easy": [
            "What is C++?",
            "What is a class?",
            "What is an object?",
            "What is inheritance?",
            "What is polymorphism?"
        ],

        "medium": [
            "What is function overloading?",
            "What is function overriding?",
            "What is encapsulation?",
            "What is abstraction?",
            "What is a constructor?"
        ],

        "hard": [
            "Explain virtual functions in C++.",
            "What is the difference between compile-time and runtime polymorphism?",
            "Explain multiple inheritance.",
            "What are pointers in C++?",
            "What is the difference between stack and heap memory?"
        ]
    },


    "ai": {
        "easy": [
            "What is Artificial Intelligence?",
            "What is Machine Learning?",
            "What is Deep Learning?",
            "What is a neural network?",
            "What is a dataset?"
        ],

        "medium": [
            "What is supervised learning?",
            "What is unsupervised learning?",
            "What is classification?",
            "What is regression?",
            "What is overfitting?"
        ],

        "hard": [
            "Explain the difference between AI, ML and Deep Learning.",
            "What is gradient descent?",
            "Explain the bias-variance tradeoff.",
            "What is a convolutional neural network?",
            "Explain the working of a neural network."
        ]
    },


    "ml": {
        "easy": [
            "What is Machine Learning?",
            "What is supervised learning?",
            "What is unsupervised learning?",
            "What is a feature?",
            "What is a dataset?"
        ],

        "medium": [
            "What is classification?",
            "What is regression?",
            "What is clustering?",
            "What is overfitting?",
            "What is underfitting?"
        ],

        "hard": [
            "Explain the bias-variance tradeoff.",
            "What is cross-validation?",
            "Explain gradient descent.",
            "What is feature engineering?",
            "How does a decision tree work?"
        ]
    },


    "dbms": {
        "easy": [
            "What is a database?",
            "What is DBMS?",
            "What is a table?",
            "What is a primary key?",
            "What is SQL?"
        ],

        "medium": [
            "What is normalization?",
            "What is a foreign key?",
            "What is a JOIN?",
            "What is a relational database?",
            "What is the difference between DELETE and DROP?"
        ],

        "hard": [
            "Explain database normalization.",
            "What are ACID properties?",
            "Explain different types of JOINs.",
            "What is database indexing?",
            "Explain transactions in DBMS."
        ]
    }
}


GENERIC_QUESTIONS = {

    "easy": [
        "What is the main concept of this topic?",
        "Why is this concept important?",
        "Where is this concept used?",
        "Can you explain this concept with an example?",
        "What are the basic features of this concept?"
    ],

    "medium": [
        "What are the advantages of this concept?",
        "What are the limitations of this concept?",
        "How does this concept work internally?",
        "How is this concept different from related concepts?",
        "Can you explain a real-world application?"
    ],

    "hard": [
        "Explain the internal working of this concept in detail.",
        "What problems can occur while implementing this concept?",
        "How would you optimize or improve this concept?",
        "Compare this concept with an alternative approach.",
        "Explain a practical scenario where this concept would be useful."
    ]
}


def normalize_subject(subject):
    subject = subject.lower().strip()

    if "data structure" in subject or subject == "dsa":
        return "dsa"

    if "python" in subject:
        return "python"

    if "java" in subject:
        return "java"

    if "c++" in subject or "cpp" in subject:
        return "c++"

    if subject == "ai" or "artificial intelligence" in subject:
        return "ai"

    if "machine learning" in subject or subject == "ml":
        return "ml"

    if "database" in subject or "dbms" in subject:
        return "dbms"

    return subject


def generate_questions(subject, topic, difficulty, number):

    subject_key = normalize_subject(subject)

    difficulty = difficulty.lower().strip()

    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = "medium"


    if subject_key in QUESTION_BANK:

        questions = QUESTION_BANK[subject_key].get(
            difficulty,
            QUESTION_BANK[subject_key]["medium"]
        )

    else:

        questions = GENERIC_QUESTIONS[difficulty]


    questions = list(questions)


    if topic:

        topic_text = topic.strip()

        if topic_text:

            topic_questions = []

            for question in questions:

                if "this topic" in question.lower():

                    topic_questions.append(
                        question.replace(
                            "this topic",
                            topic_text
                        )
                    )

                else:

                    topic_questions.append(question)


            questions = topic_questions


    if number <= len(questions):

        return questions[:number]


    result = list(questions)

    while len(result) < number:

        result.append(
            random.choice(questions)
        )

    return result


def get_correct_answer(question):

    question_lower = question.lower()


    if "binary search tree" in question_lower:

        return (
            "A binary search tree is a binary tree where the left child "
            "contains smaller values and the right child contains larger "
            "values. Searching, insertion and deletion can be performed "
            "efficiently when the tree is balanced."
        )


    if "tree traversal" in question_lower:

        return (
            "Tree traversal is the process of visiting every node of a tree. "
            "The main types are inorder, preorder and postorder traversal."
        )


    if "stack" in question_lower:

        return (
            "A stack is a linear data structure that follows the LIFO "
            "principle, meaning Last In First Out. Push and pop are common "
            "operations."
        )


    if "queue" in question_lower:

        return (
            "A queue is a linear data structure that follows the FIFO "
            "principle, meaning First In First Out. Enqueue and dequeue "
            "are common operations."
        )


    if "array" in question_lower:

        return (
            "An array is a collection of elements stored in contiguous "
            "memory locations. Elements can be accessed using an index."
        )


    if "linked list" in question_lower:

        return (
            "A linked list is a linear data structure consisting of nodes. "
            "Each node contains data and a link to another node."
        )


    if "binary search" in question_lower:

        return (
            "Binary search works on sorted data by repeatedly dividing "
            "the search space into two halves. Its time complexity is O(log n)."
        )


    if "python" in question_lower:

        return (
            "Python is a high-level, interpreted programming language known "
            "for its simple syntax and wide range of applications."
        )


    if "list" in question_lower and "tuple" in question_lower:

        return (
            "A list is mutable, meaning its elements can be changed. "
            "A tuple is immutable, meaning its elements cannot be changed "
            "after creation."
        )


    if "dictionary" in question_lower:

        return (
            "A dictionary in Python stores data as key-value pairs. "
            "It is mutable and allows fast access using keys."
        )


    if "inheritance" in question_lower:

        return (
            "Inheritance is an object-oriented programming concept where "
            "one class acquires properties and methods of another class."
        )


    if "polymorphism" in question_lower:

        return (
            "Polymorphism means one interface can have multiple forms. "
            "In programming it allows the same method or operation to behave "
            "differently depending on the object."
        )


    if "encapsulation" in question_lower:

        return (
            "Encapsulation means combining data and methods inside a class "
            "and controlling access to the internal data."
        )


    if "abstraction" in question_lower:

        return (
            "Abstraction hides unnecessary implementation details and "
            "shows only the essential features to the user."
        )


    if "machine learning" in question_lower:

        return (
            "Machine Learning is a branch of AI where systems learn patterns "
            "from data and use those patterns to make predictions or decisions."
        )


    if "supervised learning" in question_lower:

        return (
            "Supervised learning uses labelled data to train a model. "
            "Classification and regression are common supervised learning tasks."
        )


    if "unsupervised learning" in question_lower:

        return (
            "Unsupervised learning works with unlabeled data and attempts "
            "to discover hidden patterns or groups in the data."
        )


    if "classification" in question_lower:

        return (
            "Classification is a machine learning task where the model "
            "predicts a category or class."
        )


    if "regression" in question_lower:

        return (
            "Regression is a machine learning technique used to predict "
            "continuous numerical values."
        )


    if "overfitting" in question_lower:

        return (
            "Overfitting happens when a model learns the training data "
            "too closely and performs poorly on unseen data."
        )


    if "database" in question_lower:

        return (
            "A database is an organized collection of data that can be "
            "stored, accessed and managed efficiently."
        )


    if "dbms" in question_lower:

        return (
            "DBMS stands for Database Management System. It is software "
            "used to create, store, manage and retrieve data from databases."
        )


    if "primary key" in question_lower:

        return (
            "A primary key uniquely identifies each record in a table. "
            "It cannot contain duplicate values."
        )


    if "sql" in question_lower:

        return (
            "SQL stands for Structured Query Language. It is used to "
            "create, retrieve, update and manage data in relational databases."
        )


    if "algorithm" in question_lower:

        return (
            "An algorithm is a finite sequence of well-defined steps "
            "used to solve a problem."
        )


    if "data structure" in question_lower:

        return (
            "A data structure is a way of organizing and storing data "
            "so that it can be accessed and modified efficiently."
        )


    return (
        "A good answer should clearly explain the main concept, "
        "its working, important characteristics and a practical example."
    )


def evaluate_answer(question, answer):

    if AI_MODE == "demo":

        ideal_answer = get_correct_answer(question)

        answer_clean = answer.lower().strip()

        if not answer_clean:

            return {
                "score": 0,
                "feedback": "No answer was provided.",
                "ideal_answer": ideal_answer,
                "improvement": "Try to explain the main concept and give an example."
            }


        keywords = []


        question_lower = question.lower()


        if "stack" in question_lower:
            keywords = [
                "lifo",
                "push",
                "pop"
            ]

        elif "queue" in question_lower:
            keywords = [
                "fifo",
                "enqueue",
                "dequeue"
            ]

        elif "array" in question_lower:
            keywords = [
                "index",
                "memory",
                "element"
            ]

        elif "linked list" in question_lower:
            keywords = [
                "node",
                "data",
                "link"
            ]

        elif "binary search" in question_lower:
            keywords = [
                "sorted",
                "half",
                "log"
            ]

        elif "inheritance" in question_lower:
            keywords = [
                "class",
                "properties",
                "methods"
            ]

        elif "polymorphism" in question_lower:
            keywords = [
                "multiple",
                "form",
                "method"
            ]

        elif "encapsulation" in question_lower:
            keywords = [
                "data",
                "class",
                "access"
            ]

        elif "python" in question_lower:
            keywords = [
                "programming",
                "language"
            ]

        elif "machine learning" in question_lower:
            keywords = [
                "data",
                "learn",
                "model"
            ]

        elif "supervised" in question_lower:
            keywords = [
                "labelled",
                "data",
                "classification"
            ]

        elif "database" in question_lower:
            keywords = [
                "data",
                "store",
                "manage"
            ]

        else:
            keywords = [
                "concept",
                "data",
                "system"
            ]


        matched = 0

        for keyword in keywords:

            if keyword in answer_clean:

                matched += 1


        if matched == 0:

            score = 2

            feedback = (
                "Your answer needs more relevant technical points."
            )

            improvement = (
                "Start with the definition, explain the main working "
                "and include a simple example."
            )

        elif matched == 1:

            score = 5

            feedback = (
                "You mentioned one important point, but the explanation "
                "needs more technical details."
            )

            improvement = (
                "Add more key concepts and explain how the concept works."
            )

        elif matched == 2:

            score = 7

            feedback = (
                "Good answer. You included important technical points."
            )

            improvement = (
                "Add a practical example and explain the concept more clearly."
            )

        else:

            score = 9

            feedback = (
                "Excellent answer. You covered the major technical points."
            )

            improvement = (
                "For an even stronger viva answer, add a real-world example."
            )


        return {
            "score": score,
            "feedback": feedback,
            "ideal_answer": ideal_answer,
            "improvement": improvement
        }


    return {
        "score": 0,
        "feedback": "AI evaluation mode is not configured.",
        "ideal_answer": get_correct_answer(question),
        "improvement": "Configure AI mode to enable advanced evaluation."
    }


def generate_follow_up_question(
    original_question,
    answer,
    score
):

    answer_lower = answer.lower()

    question_lower = original_question.lower()


    if score >= 8:

        followups = [

            "Can you give a real-world example of this concept?",

            "Why is this concept useful in practical applications?",

            "What would happen if this concept was not used?",

            "Can you explain one limitation of this approach?"

        ]


    elif score >= 5:

        followups = [

            "Can you explain that concept in more detail?",

            "Can you give a simple example?",

            "Why is this concept important?",

            "What are the main advantages of this concept?"

        ]


    else:

        followups = [

            "Can you explain the basic definition of this concept?",

            "Can you give a simple example?",

            "What is the main purpose of this concept?",

            "Where is this concept commonly used?"

        ]


    if "stack" in question_lower:

        if "lifo" in answer_lower:

            return "Can you give a real-world example where the LIFO principle is used?"

        return "What principle does a stack follow?"


    if "queue" in question_lower:

        if "fifo" in answer_lower:

            return "Can you give a real-world example where the FIFO principle is used?"

        return "What principle does a queue follow?"


    if "array" in question_lower:

        return "What is one advantage of using an array?"


    if "linked list" in question_lower:

        return "What is one advantage of a linked list over an array?"


    if "inheritance" in question_lower:

        return "What is one major advantage of inheritance?"


    if "polymorphism" in question_lower:

        return "Can you explain the difference between compile-time and runtime polymorphism?"


    if "machine learning" in question_lower:

        return "Can you give a real-world application of Machine Learning?"


    if "supervised learning" in question_lower:

        return "Can you give an example of a supervised learning algorithm?"


    if "overfitting" in question_lower:

        return "How can you reduce overfitting in a machine learning model?"


    if "database" in question_lower:

        return "Why are databases preferred over storing large amounts of data in simple files?"


    if "sql" in question_lower:

        return "Can you give an example of a SQL query used to retrieve data?"


    return random.choice(followups)