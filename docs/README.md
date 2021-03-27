# Byzantine-Resilient Distributed Hypothesis Testing With Time-Varying Network Topology

## Bo Wu, Steven Carr, Suda Bharadwaj, Zhe Xu, and Ufuk Topcu

### Synchronous vs Asynchronous Updating

{% include youtube_sync.html %}


{% include youtube_async.html %}

### Minimum vs Averaging Update Rules

{% include youtube_min.html %}

{% include youtube_average.html %}

### Large Case Study - 12 Agents (2 coordinating bad actors)

The expanded case study for "Byzantine-Resilient Distributed Hypothesis Testing With Time-Varying Network Topology".  10  good  agents  and  2  coordinating nefarious  actors.  The two coordinating agents are sharing the same false hypothesis to their neighbors in the system.
The line plot shows the averaged local belief (LB) and actual belief (AB) over the 10 good agents at any given time. Both lines will eventually converge to 1 but with ADHT the AB converges more quickly despite the 2 coordinated nefarious agents transmitting false hypothesis data.

The dip at t=175 is due to both bad actors sharing with an agent that has performed an incorrect observation, briefly causing that agent to incorrectly infer that the system is in the false hypothesis broadcasted by the 2 bad agents. Once the agent has accumulated sufficient information from the other good agents, it quickly converges back to the correct hypothesis.

{% include youtube_large.html %}
