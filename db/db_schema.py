# Design stage
#general data base: list of dicts by coubtry

[{'country name':{''}]
# data-base schema for research announcements by country 
# v1.
{  
    "country":'str',
    "announcements_metadata":'list'
    "announcements":'list of dicts(announcements)' # Each announcement plus document key
}
# v2.
{  
    "announcements_metadata":'list'
    "announcements":'list of dicts(announcements)' # Each announcement plus document key
}

# data-base schema for each document by research announcement
# v1.

{
    "idx":"int", # Index of announcement that document belong
    "section_#":'str',
    "entire_text":'str' 
}

# v2
{
    "idx":"int",
    "metadata": 'dict', # atributes and values. e.g 'title':'value title' etc
    "body_text": 'list of dict' # [{'text':'str','section':'str'} ...] index of list is num of paragraph.
}

# v3: best candidate.

{
    "metadata": 'dict', # atributes and values. e.g 'title':'value title' etc
    "body_text": 'list of dict' # [{'text':'str','section':'str'} ...] index of list is num of paragraph.
}

# not select for now. thinking about it...

# Implementation
# Example of one record general db: with schema v2 for research announcements and v3 for documents
# one country with two announcement, the firts with two documents asociated, two with three;
{
    'Colombia':{
            "announcements_metadata":['title','objs','funds', 'links pdf'],
            "announcements":[

                                {
                                    'title': 'value title',
                                    'objs': 'value objs',
                                    'funds': 'value funds',
                                    'link pdfs':'value links pdfs',
                                    'documents':[

                                        {
                                            "metadata": { 
                                                            'title':'value title',
                                                            'date': 'value date'

                                                        }
                                            "body_text": [  {'text':'str','section':'str'},
                                                            {'text':'str','section':'str'}
                                                                        ] 
                                        },

                                        {
                                            "metadata": { 
                                                            'title':'value title',
                                                            'date': 'value date'

                                                        }
                                            "body_text": [  {'text':'str','section':'str'},
                                                            {'text':'str','section':'str'}
                                                                        ] 
                                        }
                                    ]
                                },

                                {
                                    'title': 'value title',
                                    'objs': 'value objs',
                                    'funds': 'value funds',
                                    'link pdfs':'value links pdfs',
                                    'documents':[

                                        {
                                            "metadata": { 
                                                            'title':'value title',
                                                            'date': 'value date'

                                                        }
                                            "body_text": [  {'text':'str','section':'str'},
                                                            {'text':'str','section':'str'}
                                                                        ] 
                                        },

                                        {
                                            "metadata": { 
                                                            'title':'value title',
                                                            'date': 'value date'

                                                        }
                                            "body_text": [  {'text':'str','section':'str'},
                                                            {'text':'str','section':'str'}
                                                                        ] 
                                        },

                                        {
                                            "metadata": { 
                                                            'title':'value title',
                                                            'date': 'value date'

                                                        }
                                            "body_text": [  {'text':'str','section':'str'},
                                                            {'text':'str','section':'str'}
                                                                        ] 
                                        },
                                    ]
                                }
                            ]
                        }
}

# Example of queries
db['Colombia'] -> 'dict with all announcements'
db['Colombia']['announcements'] -> 'list of dicts' 
db['Colombia']['announcements'][0]['title'] ->'str title of anouncement'
db['Colombia']['announcements'][0]['documents'][0] -> 'dict with metadata and body text of firts document first announcement' 
db['Colombia']['announcements'][0]['documents'][1] -> 'dict with metadata and body text of second document of firts announcement'
db['Colombia']['announcements'][0]['documents'][0]['text'] -> 'str with text of first paragraph of firts document of firts announcement'
