Surfiki Refine for Elasticsearch (Non Distributed Version) - If you are interested in the distributed version of Refine, please contact Intridea.


Python Map-Reduce Transformation/Extraction/Manipulation Tier for Elasticsearch Indices

#####Part of the Surfiki Data Engine
- [Surfiki REBIN](http://intridea.github.io/REBIN/)
- [Surifki Developer API](http://developer.surfiki.com/)
- [Surfiki.com](http://www.surfiki.com)


##What is Refine?


Originally designed to work with Elasticsearch indices and API. Refine allows you to take an input stream, transform and or manipulate it for your needs, then output it in a variety of formats.


With the variety of uses of Elasticsearch being seen in the its ecosystem (Search, Data Stores, API), a powerful and extensible processing tier was needed to meet Intridea’s needs. Our belief, is this can fit in to your Elasticsearch environment as well. And in turn, provide you with additional transformation and or manipulation capabilities.


At its heart, Refine is a collection of scripts, written by you in Python.


##How does it work?


Technically, Refine is Map-Reduce, which for each job you define incorporates:


A stream script defines the source of your data. A query’s results (In the case of Elasticsearch) A file or files, or a Web API such as Twitter.


 - A mapper script takes the input, divides it into smaller sub-problems, and distributes them to workers. 


 - A worker may do this again in turn, leading to a multi-level tree structure. The worker processes the smaller problem, and passes the answer back to its master.


 - A reducer script collects the answers to all the sub-problems and combines them in some way to form the output – the answer to the problem it was originally trying to solve.


 - You can add as many scripts that your job may require, however the core is the stream, mapper and reducer scripts.
 
##What are some cool features?

- Online Browser based code editing, job management and results collection.

- Job Testing (Syntax & Job functions)

- Job Scheduling

- Job Duplication

- Live CLI

<a href="http://www.flickr.com/photos/95752811@N04/8738542001/" title="refine1 by NyströmAnthony, on Flickr"><img src="http://farm8.staticflickr.com/7286/8738542001_8b182dfcde.jpg" width="376" height="345" alt="refine1"></a>
<a href="http://www.flickr.com/photos/95752811@N04/8738542005/" title="refine2 by NyströmAnthony, on Flickr"><img src="http://farm8.staticflickr.com/7285/8738542005_763e502a33.jpg" width="376" height="345" alt="refine2"></a>
<a href="http://www.flickr.com/photos/95752811@N04/8739661106/" title="refine3 by NyströmAnthony, on Flickr"><img src="http://farm8.staticflickr.com/7283/8739661106_1894aec094.jpg" width="376" height="345" alt="refine3"></a>
<a href="http://www.flickr.com/photos/95752811@N04/8738541955/" title="refine4 by NyströmAnthony, on Flickr"><img src="http://farm8.staticflickr.com/7282/8738541955_ccac2229ee.jpg" width="376" height="345" alt="refine4"></a>

##What are some examples?


- Combining data from multiple indices in to a new index. With Refine you can either do this ad hoc or on a scheduled basis.


- Splitting data from a single index in to new indices based upon some criteria. Refine makes this relatively simple to perform.


- Statistical facets can be taxing on the heap. You can use Refine to process/transform/count this data and expose within a new index on a set schedule.


- Transforming data already indexed with additional data. For example, some data has location information (lat, long) however you also want to store meta data associated with those locations Such as State, City and County information. While it makes sense to do some of this in line, with Refine you can do it after the initial data is already indexed.


- Accessing third party API's to append data to existing indexed data. With Refine, accessing those API’s, injecting and or manipulating is a core feature.


- Given a body of text, you can use Refine to split your stream into its separate words, perform a word count for the given word, then reduce it to a de-duped sorted array.


- Given a collection of results, you can use Refine to further score each result against a series of 
validation criteria such as geographic region or category.


- Need text to appear in various ways, before it can be processed further? Use Refine to prepend suffixes or concatenate strings, and dynamically add these as new attributes.


###Open Source Projects utilized:


- [redis](http://redis.io/)

- [Paramedic](https://github.com/karmi/elasticsearch-paramedic)

- [Sense](https://github.com/bleskes/sense)

- [r3](https://github.com/heynemann/r3)

- [Python Dev Bootstrap](http://anthonynystrom.github.io/python-dev-bootstrap/)

- [Lookout](https://github.com/delan/lookout)

- [Flask](http://flask.pocoo.org/)

- [Twitter Bootstrap](http://twitter.github.io/bootstrap/)

- [Cloud9](https://github.com/ajaxorg/cloud9/)

- [Python](http://python.org/)

- [PyFlakes](https://pypi.python.org/pypi/pyflakes)

- [ujson](https://pypi.python.org/pypi/ujson)

- [pyes](https://github.com/aparo/pyes)

- [node.js](http://nodejs.org/)

Special Mention:

Many thanks go out to Bernardo Heynemann for his excellent work with r3.


---


##Installation Instructions

The editor portion of Refine uses a specific version of node.js:

	Install node.js v0.6.21

	Install source mint globally
	$ npm install -g sm

	Install and build modules 
	$ cd cloud9
	$ sm install

	Install cloud9 as an upstart job 
	$ cp cloud9.conf /etc/init/
	$ start cloud9

##Usage Instructions

