""" IDEA:
      We want our Markov Chain to look at the last n pixels to decided the
      next pixel to place. But what if that sequence doesn't appear in the
      Markov Chain already?
      Try defining a metric on the space of n-tuples of RGB values. Then, 
      if the sequence isn't in our chain, find the closest sequence!
"""
