"""
Replication of :
   TALENT VERSUS LUCK: THE ROLE OF RANDOMNESSIN SUCCESS AND FAILURE,
   Advances in Complex Systems, 2018
   PLUCHINO, BIONDO, and RAPISARDA
   DOI:10.1142/S0219525918500145

by :
 Jeremy Lefort-Besnard


This model tries to evaluate the importance of chance in success 
compared to talent alone. The results challenge the dominant
meritocratic paradigm of highly competitive Western cultures.
We see through the simulation results that advantage of having 
a great talent is a necessary,but not a suficient, condition to 
reach a very high degree of success.

"""

import numpy as np
import matplotlib.pyplot as plt
import math


class build_world:
  def __init__(self, N, Ne):

    # define people
    self.N = N
    self.Ne = Ne
    self.people_loc = np.array([np.random.uniform(0,1,N), np.random.uniform(0,1,N)])
    self.people_talent = np.random.normal(0.6,0.1,N)
    self.people_talent[np.where(self.people_talent < 0)] = 0.6
    self.people_talent[np.where(self.people_talent > 1)] = 0.6

    self.people_capital = np.array([10.0] * N)

    # define environment
    self.half_Ne = int(self.Ne/2)
    self.event_loc = np.array([np.random.uniform(0,1,Ne), np.random.uniform(0,1,Ne)])
    self.event_pos = np.random.uniform(0,1,self.half_Ne) * 100
    self.event_neg = 100 - self.event_pos

  def display_talent(self):
    fig = plt.figure(figsize = (10, 5))
    plt.title("Talent distribution")
    plt.hist(self.people_talent, bins=50)
    plt.xlabel("Talent at birth")
    plt.ylabel("Number of individuals")
    plt.show()

  def display_world(self):
    plt.scatter(self.people_loc[0], self.people_loc[1], color = "blue", alpha=0.5, marker =2)
    plt.scatter(self.event_loc[0][:self.half_Ne+1], self.event_loc[1][:self.half_Ne+1], color = "green",alpha=0.5, marker ='^', s=15)
    plt.scatter(self.event_loc[0][self.half_Ne:], self.event_loc[1][self.half_Ne:], color = "red",alpha=0.5, marker ='v', s=15)
    plt.axhline(0, color='black')
    plt.axhline(1, color='black')
    plt.axvline(0, color='black')
    plt.axvline(1, color='black')
    plt.grid(visible=False)
    plt.axis('off')
    plt.show()

  def display_world_eventhappening(self):
    plt.scatter(self.people_loc[0], self.people_loc[1], color = "blue", alpha=0.5, marker ='o')
    plt.scatter(self.event_loc[0][:self.half_Ne+1], self.event_loc[1][:self.half_Ne+1], color = "green",alpha=0.5, marker ='^')
    plt.scatter(self.event_loc[0][self.half_Ne:], self.event_loc[1][self.half_Ne:], color = "red",alpha=0.5, marker ='v')
    for people_ind in self.event_per_guy:
      if self.event_per_guy[people_ind] != []:
        plt.scatter(self.people_loc[0][people_ind], self.people_loc[1][people_ind], color = "yellow", alpha=0.5, marker ='X')
    plt.axhline(0, color='black')
    plt.axhline(1, color='black')
    plt.axvline(0, color='black')
    plt.axvline(1, color='black')
    plt.grid(visible=False)
    plt.axis('off')
    plt.show()



  def pick_closest_event(self):
    self.event_per_guy = {}
    for ind_people, people_x in enumerate(self.people_loc[0]):
      events_per_guy = []
      # check which events are around each person
      for ind_event, event_x in enumerate(self.event_loc[0]):
        event_y = self.event_loc[1][ind_event]
        people_y = self.people_loc[1][ind_people]
        if (matching_location(event_x, event_y, people_x, people_y)):
          events_per_guy.append(ind_event)
      # pick only the clostest event
      if len(events_per_guy) > 1:
          picked_event = closest_event([people_x, people_y], events_per_guy)
          events_per_guy = [picked_event]
      self.event_per_guy[ind_people] = events_per_guy
    return self.event_per_guy


  def apply_event_effect(self):
    for ind_people in self.event_per_guy:
      # event happening 
      if self.event_per_guy[ind_people] != []:
        # happy event
        if self.event_per_guy[ind_people][0] < self.half_Ne:
          # talented enough to profit the chance
          if self.people_talent[ind_people] > np.random.rand():
              self.people_capital[ind_people] *= 2
        # unhappy event
        else:
          self.people_capital[ind_people] /= 2



  def life_goes_on(self, step=0.02):
    directions = np.random.randint(0, 360, self.N)
    new_people_loc_x = []
    new_people_loc_y = []
    for ind, pos in enumerate(self.people_loc[0]):
      new_x = pos + step*math.cos(math.radians(directions[ind]))
      new_y = self.people_loc[1][ind] + step*math.sin(math.radians(directions[ind]))
      if new_x > 1:
        new_x = -1 + new_x
      if new_y > 1:
        new_y = -1 + new_y
      if new_x < 0:
        new_x = 1 + new_x
      if new_y < 0:
        new_y = 1 + new_y
      new_people_loc_x.append(new_x)
      new_people_loc_y.append(new_y)
    self.people_loc = np.array([new_people_loc_x, new_people_loc_y])

  def display_metrics(self):
    talent_capital = sorted(list(map(lambda x : [x[0], x[1]],zip(self.people_talent,self.people_capital))))
    talent = np.array(talent_capital).T[0]
    capital = np.log10(np.array(talent_capital).T[1])+ np.log10(np.array(talent_capital).T[1]).min() * -1
    fig = plt.figure(figsize = (10, 5))
    plt.bar(talent, capital, color ='maroon',
        width = 0.001)
    plt.axvline(np.median(self.people_talent), color='red')
    plt.axvline(self.people_talent.max(), color='black')
    plt.axvline(self.people_talent.min(), color='black')
    plt.xlabel("Talent at birth")
    plt.ylabel("Capital after 40 years")
    plt.title("relationship capital vs talent")
    plt.axis('on')
    plt.show()

  def display_results(self):
    # talent_capital = sorted(list(map(lambda x : [x[0], x[1]],zip(self.people_talent,self.people_capital))))
    # capital = np.array(talent_capital).T[1]
    talent = self.people_talent
    capital = self.people_capital
    fig = plt.figure(figsize = (10, 5))
    plt.scatter(talent, capital, color ='green', alpha=0.5, s=3)
    plt.yscale('log')
    plt.xlabel("Talent at birth")
    plt.ylabel("Capital after 40 years")
    plt.title("Talent versus capital")
    x_ticks= [0.3, 0.45, 0.6, 0.75, 0.9]
    plt.xticks(ticks=x_ticks, labels=['Ridiculous', 'Bad', 'Average', 'Good', 'Top'])
    y_ticks= [0.1, 10, 10**3, 10**11, capital.max()]
    plt.yticks(ticks=y_ticks, labels=['Debts', '10 $', '1000 $', '100 billions $', '1000 billions $'])
    plt.axhline(0.1, color='grey', linewidth=0.5)
    plt.axhline(10, color='grey', linewidth=0.5)
    plt.axhline(1000, color='grey', linewidth=0.5)
    plt.axhline(capital.sum()*0.2, color='blue', linewidth=0.5) # 20% of the wealth
    plt.text(0.3, 10**16, '20% of the wealth, {}% of the population'.format(sum(capital<capital.sum()*0.2)*100/len(capital)), color='blue', size=8)
    plt.text(0.3, 1, '{}%'.format(sum(capital<10) * 100 / len(capital)), color='black', size=8)
    plt.text(0.3, 0.01, '{}%'.format(sum(capital<0.1) * 100 / len(capital)), color='black', size=8)
    plt.text(0.3, 900, '{}%'.format(sum(capital<1000) * 100 / len(capital)), color='black', size=8)
    plt.axis('on')
    plt.tight_layout()
    plt.show()



    
def matching_location(circle_x, circle_y, x, y):
  # Compare radius of circle
  # with distance of its center
  # from given point
  rad = 0.03
  if ((x - circle_x) * (x - circle_x) +
      (y - circle_y) * (y - circle_y) <= rad * rad):
      return True;
  else:
      return False;

def distance_event(coord_person, coord_event):
  return np.linalg.norm(np.array(coord_person) - np.array(coord_event))

def closest_event(coord_person, coord_events):
  closest_event = None
  for coord_event in coord_events:
    if closest_event == None:
      closest_event = coord_event
    elif distance_event(coord_person, coord_event) < closest_event:
      closest_event = coord_event
  return closest_event


# Rewrite the y labels

run = build_world(1000, 500)
run.display_talent()
run.display_world()

for i in range(1, 81, 1):
  if i<20:
    if i%2==0:
      print("year: 200{}".format(int(i/2)))
  else:
    if i%2==0:
      print("year: 20{}".format(int(i/2)))
  run.pick_closest_event()
  run.apply_event_effect()
  run.life_goes_on()
run.display_world()
# run.display_metrics()
run.display_results()







# fig = plt.figure(figsize = (10, 5))
# plt.title("capital per individuals")
# plt.hist(run.people_capital, 
#     bins=[0, 100, 250, 500,1000, 1500, 2000, 2500, 3000], 
#     width=10, color='maroon')
# plt.yscale('log')
# plt.xscale('linear')
# plt.ylabel('Nb of individuals')
# y_ticks= [1, 10, 100, 500, 1000]
# plt.yticks(ticks=y_ticks, labels=y_ticks)
# plt.xlabel('Capital/talent')
# plt.xlim(0, 3000)
# plt.show()



# f, ([ax1, ax2],[ax3, ax4]) = plt.subplots(2, 2, figsize=(10, 10)) 

# talent_capital = sorted(list(map(lambda x : [x[0], x[1]],zip(run.people_talent,run.people_capital))))
# talent = np.array(talent_capital).T[0]
# capital = np.array(talent_capital).T[1]

# # bargraph
# ax1.scatter(talent, capital, color ='maroon')
# ax1.axvline(np.median(run.people_talent), color='red')
# ax1.axhline(10, color='black', linestyle='dotted')
# ax1.set_yscale('log')
# ax1.set_xlabel("Talent at birth")
# ax1.set_ylabel("Capital after 40 years")
# ax1.set_title("Capital versus talent")
# y_ticks= [0.1, 10, 10**3, 10**11, capital.max()]
# ax1.set_yticks(ticks=y_ticks, labels=['0.1 $', '10 $', '1000 $', '100 billions $', '1000 billions $'])
# ax1.axis('on')


# ax2.scatter(capital, talent, color ='green', alpha=0.5, s=3)
# ax2.set_xscale('log')
# ax2.set_xlabel("Capital after 40 years")
# ax2.set_ylabel("Talent at birth")
# ax2.set_title("Talent versus capital")
# y_ticks= [0.3, 0.6, 0.9]
# ax2.set_yticks(ticks=y_ticks, labels=['Low skils', 'Average skills', 'Top skills'])
# ax2.axvline(10, color='grey')
# ax2.axvline(capital.sum()*0.8, color='red') # 80% of the wealth
# ax2.axvline(capital.sum()*0.1, color='blue') # 10% of the wealth
# ax2.text(10**19, 0.9, '<- 80% ->', color='red', size=8)
# ax2.text(10**7, 0.9, '<- 10% of the wealth ->', color='blue', size=8)
# ax2.axis('on')



# # histogram
# ax3.hist(run.people_capital, 
#     bins=[0, 10, 100, 250, 500,1000, 1500, 2000, 2500, 3000], 
#     width=10, color='blue')
# ax3.set_title("Capital distribution among population")
# ax3.set_yscale('log')
# ax3.set_ylabel('Nb of individuals')
# y_ticks= [1, 10, 100, 500, 1000]
# ax3.set_yticks(ticks=y_ticks, labels=y_ticks)
# ax3.set_xlabel('Capital/sucess')
# ax3.set_xlim(0, 3000)

# plt.tight_layout()
# plt.show()