import random

def startGamble(bandit):
  random_normal = -1
  while random_normal <= 0:
    random_normal = random.gauss(bandit[0], bandit[1])
  return random_normal

def chooseBandit(reward1, reward2):
  if abs(reward1-reward2) <= 10:
    ran = random.randint(0,99)
    if ran == 50:
      if reward1 > reward2:
        return 2
      else:
        return 1
  if reward1 > reward2:
    return 1
  elif reward1 < reward2:
    return 2
  else:
    return random.randint(1,2)

def startLearning():
  bandit1 = (500, 50)
  bandit2 = (550, 100)
  gambleTime = 100000
  reward1 = 1000
  reward2 = 1000
  cnt1 = 1
  cnt2 = 1
  for _ in range(gambleTime):
    if chooseBandit(reward1,reward2) == 1:
      r = startGamble(bandit1)
      reward1 = ((reward1 * cnt1) + r)/(cnt1+1)
      cnt1 += 1
    else:
      r = startGamble(bandit2)
      reward2 = ((reward2 * cnt2) + r)/(cnt2+1)
      cnt2 += 1
  print(reward1,reward2)

def main():
  startLearning()

if __name__ == '__main__':
  main()
