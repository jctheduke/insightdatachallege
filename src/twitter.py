import json                   # for parsing json files
from time import strptime     # For matching time format
from time import mktime       # For converting time to timestamp
from itertools import combinations  #For performing nchoosek operations
from heapq import heappush    # For maintaining a min-heap
from heapq import heappop
import codecs                  #For converting the codecs

f=open('./tweet_input/tweets.txt','r+')  #open the given twitter file
f1=open('./tweet_output/ft1.txt', encoding='ascii', mode='w+')
f2=open('./tweet_output/ft2.txt', encoding='ascii', mode='w+')
tweets=[]   # For storing the tweets
count=0     # For counting the number of tweets needed to be changed
graph={}    # For storing #hashtags in a graph
heap=[]     # Initializing the min-heap
for x in f.readlines():
    js=json.loads(x)
    try:
        if isinstance(js['text'],str):                             # Checks if the current text is unicode
            count+=1                                               # Counts no of strings that needed conversion
        timestamp=js['created_at']                                 # Collects the timestamp from the json file
        current_time=strptime(timestamp,'%a %b %d %H:%M:%S %z %Y') # Formatting it to time_structure
        current_timestamp=mktime(current_time)                     # Converting time to timestamp in seconds
        text="".join(filter(lambda x:ord(x)<128,js['text']))   # Converts the string if it's unicode
        if len(text)>1:                                            # Checks for empty tweets
            tweet="{} ({})".format(text,timestamp)                 # Records tweet in the desired format
            f1.write("%s\n"%tweet)                                 # writing tweets to f1 as requested in feature 1
            e=js['entities']                                       # Extracting hash tags
            tagl=e['hashtags']
            if (tagl):                                              # Checking for empty Hash-tags
                tag=[]
                for l in tagl:
                    tag_unicode=l['text']
                    tag_ascii="".join(filter(lambda x:ord(x)<128,tag_unicode))  # cleaning hash-tags
                    tag.append(tag_ascii)                                       # collection of all hash-tags with in a tweet
                if len(tag)>1:
                    Hashtags=list(combinations(tag,2))                          # Getting all 2 pair combinations of Hash-tags
                    for t in Hashtags:                                          # Adding hash-tag pairs as edges to the graphs
                        if t[0] not in graph.keys():
                            graph[t[0]]=[t[1]]
                        else:
                            graph[t[0]].append(t[1])
                        if t[1] not in graph.keys():
                            graph[t[1]]=[t[0]]
                        else:
                            graph[t[1]].append(t[0])
                    heappush(heap,(current_timestamp,Hashtags))                # Keeping track of the hash-tags that are added to graph at current time
        try:
            # Removal of hash-tags pairs which are older that 60 seconds
            if current_timestamp-(heap[0])[0]>60:
                for i in heappop(heap)[1]:
                    graph[i[0]].remove(i[1])
                    graph[i[1]].remove(i[0])
                    if len(graph[i[0]])==0:
                        del graph[i[0]]
                    if len(graph[i[1]])==0:
                        del graph[i[1]]
        except IndexError:
            pass
    except KeyError:
        pass
    nodes=0
    edges=0
    # Calculating degree for the second feature
    for x,y in graph.items():
        nodes+=1
        edges+=len(set(y))
    try:
        degree=(edges/nodes)
        f2.write("%s\n"%degree)
    except ZeroDivisionError:
        degree=0
        f2.write("%s\n"%degree)
f1.write('%s tweets contained unicode'%count)
f1.close()
f2.close()
f.close()