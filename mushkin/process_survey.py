from collections import Counter
import csv

def get_formatted(title, counts):
    output = title + '\n'
    sorted_responses = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for response, number in sorted_responses:
        proportion = str(number) + '/' + str(responders)
        percentage = str(round(100*number/float(responders), 1)) + '%'
        output += proportion + ' (' + percentage + ') ' + response + '\n'
    return output    

if __name__=='__main__':
    responses = []

    with open('responses.csv', 'rb') as csvfile:
        responses = list(csv.reader(csvfile, delimiter=','))

    cdict  = {}
    titles = responses[0]
    responders = len(responses)-1

    # things to ignore
    ignore = ['Timestamp']
    
    # create a bunch of counters
    for title in titles:
        if title in ignore: continue
        cdict[title] = Counter()

    # count things
    for row in responses[1:]:
        for i,response in enumerate(row):
            if titles[i] in ignore: continue
            cdict[titles[i]][response] += 1

    # rectify counts for multiple-choice questions
    mc_titles = ['What learning format(s) would you prefer?',
                 'What happens when it\'s over?',
                 'What\'s the goal?',
                 'What term should this workshop series happen?',]
    for title in titles:
        if title in ignore: continue
        if title in mc_titles:
            # split each line by commas
            for key in cdict[title].keys():
                c = cdict[title][key]
                del cdict[title][key]
                for option in key.split(','):
                    option = option.strip()
                    cdict[title][option] += c

    skill_titles = []
    other_titles = []
    for title in titles:
        if 'Skills you have' in title:
            skill_titles.append(title)
        else: other_titles.append(title)

    skill_titles = sorted(skill_titles,
                                 key=lambda x: cdict[x]['Would like to know'],
                                 reverse=True)
            
    # format and print
    for title in other_titles + skill_titles:
        if title in ignore: continue
        print get_formatted(title, cdict[title])
