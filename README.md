# Agar.io_Q-Learning_AI
An experiment on the performance of homemade Q-learning AIs in Agar.io depending on their state representation and available actions.

An image of the circle categorisation function in action. Food blobs are outlined in blue, edible cells in green and dangerous cells in red according to where our program detects them. Screen edges mess that up a bit. The agents action at this moment is labelled with the green arrow.
![Circle Detection Diagram drawio](https://user-images.githubusercontent.com/98162688/150537743-c788f4de-223d-44ce-a2d3-ffdec4095b87.png)

States are calculated using the shortest euclidian distance to each of the three circle types: food, edible cells and dangerous cells. These distances are measured and discretized according to which interval they fall within. The rulers in this image are to scale.
![State Pic](https://user-images.githubusercontent.com/98162688/150537757-bfd71e01-7c79-40ae-857a-cc9fa296df26.png)

Currently the agent can't press any keyboard buttons, only move around using the mouse. It could be added without too much hassle, but it would require a rework of some aspects of the code and a ton training, which already takes ages. The q-learning part could also do with a proper implementation of stochastic q-learning instead of our generic iterative q-learning, if I knew how to do it. I look forward to learning that at a later point.

Feel free to ask any questions about the code or the project. I hope you enjoy!
