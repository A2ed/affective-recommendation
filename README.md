# Affective recommendation: generating product recommendations based on emotional states

# Synopsis

This project develops a recommendation engine using of the most central, but often overlooked, determinants of decision making: affective reasoning. It operates by querying a person's emotional state and using a deep learning model to identify products similar to that state. This differs from conventional recommendation engines that rely on demographic information and historic purchase trends, and aims to recontextualize the buying process from acquisition of a particular product to the generation of a particular experience.

# Why emotions?

In 1979, two psychologists published a paper desribing a theory of decision making that would form the basis of modern economic thinking. Termed [**prospect theory**](https://en.wikipedia.org/wiki/Prospect_theory), the paper by Daniel Kahneman and Amos Tversky articulated a vision of people evaluating and conducting decisions based on information that has been shaped by a series of mental biases and heuristics. A complete enumeration of cognitive biases is beyond the scope of this documentation, but interested readers can check them out [**here**](https://en.wikipedia.org/wiki/List_of_cognitive_biases). One of the types of information relevant to biases that prospect theory attempts to model is affective forecasting, most prominently in the form of projection bias. This idea suggests that emotional states influence how we evaluate future states and that biases using emotional information can motivate or demotivate an individual towards making decisions to achieve desired outcomes.

# Recommendations in their current state

One of the primary information filters affecting product selection online is constraints around a UI. When a person visits Amazon or Netflix, there is only so much space on a screen to present choices. This has led market differentiation based on the capacity of a company to put highly salient and relevant information in front of a customer. Websites like those of Netflix and Amazon are largely recommendation systems that optimize around internal KPIs such as user engagement. However, the data that they operate on tends to be collaborative (i.e. if two users have similar historic data, they will have similar preferences) or item based (i.e. what two products, even across different categories, are the most similar). While unquestionably successful (I'm looking at you, Jeff Bezos), modeling person-to-person and item-to-item similarity suggests that there may be another axis to generate product recommendations from, namely experience-to-experience. 

# Affective recommendations

When you look at successful lifestyle companies like Nike and Apple, or marketing gurus like Seth Godin, the idea from prospect theory that emotions color our purchase decisions showcases how much people will bias spending to obtain a particular experience. In fact, people like Seth Godin go as far to say that people buy purely based on how they expect a product to make them feel. This is captured in behavioral patterns such as retail therapy and how social media companies can optimize presentation of media based on elicitation of emotional states. 

Turning our attention towards product recommendaitons, I wanted to develop an engine that bypassed proxies of affective reasoning and targeted it directly. To that end, the engine available here queries a person's emotional state and uses that information to calculate similarity scores with product meta data. In the langauge of behavioral economics, this would be purchasing based on immediate, integral emotions (i.e. ones that are direct to a person's current experience), and not expected emotions. The reason for this is projection bias - that a person's current emotional state colors what they percieve to be likely future states. However, by changing the prompt for input data, the affective target can easily be changed to expected emotions.

> Immediate emotion: How are you feeling right now?

> Expected emotion: How are you wanting to feel in the future?

# Overview of recommendation engine

Complete details of the engine are in the engine.ipynb. The code in the notebook was refactored into the class RecommendationEngine in affective_rec.py. As an overview, the engine does the following:

1. Receives an input emotion
2. Checks to see if the emotion is stored in the dictionary of emotions (parent) and synonyms (children)
3. If so, it returns the parent emotion
4. If not, it uses SpaCy to calculate cosine distance similarity scores between the input emotion and the parent/children emotions and returns the top parent emotion
5. Uses parent emotion to find top three scotches based on cosine distance similarity scores with product meta data
6. Returns meta data for the top product recommendations

# Word embeddings and similarity scores

The bulk of the computation of the engine relies on word embeddings. Word embeddings are generally thought of as numeric representations of sematic information that can be used to describe both the general intent (i.e. the target reference) of a word and the context in which it occurs. Importantly, embeddings create word/sentence level representations in a high dimensional space that allow us to calculate how similar or close a particular data instance is from another. 

A more granular view of the information flow through the recommendation engine is as follows. The UI queries a person's emotional state. This can be anything from happy, to melodramatic, to pensive or somber. The engine then searches a dictionary of common emotions to see if there is a match. The common emotions in the dictionary are paired with synonyms from the open source [**Moby thesauras**](https://github.com/words/moby). The rationale to couple an emotional input with synonyms is that when we calcualte the document level embeddings (here, the parent emotion and the children synonyms), there is more diversity in the representation of the potential reference and context. If there is no match, the engine will calculate the cosine similarity between the input embedding and the document embeddings of the parent/child emotions in the dictionary. The dictionary emotions were selected to reflect the [**emotional primitives**](https://people.ece.cornell.edu/land/OldStudentProjects/cs490-95to96/HJKIM/emotions.html) that are universal across cultures.

Once the most appropriate parent emotion is found, the engine queries a database of cosine similarity scores between the document embeddings for the parent/child emotions and meta desriptions of a product. In its current iteration, the engine then returns the top twenty five matches and randomly subsamples three to present some variation at the user experience level. 

# Demo: Scotchy Scotch - recommending scotches based on emotional states

The main engine is a class contained in affective_rec.py. It is fairly easy to tweak but send me a message if anything isn't clear.

As a demo use case, I used the engine to create a Django app to recommend scotches based on a person's emotional state. At the top of affective_rec.py, there are paths to the data the engine needs and the parts that I precomputed based on this use case to speed up the user experience. This repo also contains the necessary code for Scotchy Scotch and should be easy to replicate. The quickest way to do that is to build a docker image from the dockerfile and use docker compose to create the container for the app to run in.
