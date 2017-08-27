from random import randint, random, seed, shuffle
from sys import argv

SEED = 0
PS = 500
IT = 600
CP = 0.9
MP = 0.1
ELITE = int(0.05 * PS)

class Instance:
    """Class representing an instance of the JSP."""
    def __init__(self, jobs, m):
        self.jobs = jobs
        self.n = len(jobs) # number of jobs
        self.m = m         # number of machines

    def __getitem__(self, i):
        return self.jobs[i]

    def __len__(self):
        return len(self.jobs)


def LoadInstance(fname):
    """Load instance file."""
    f = open(fname, 'r')
    head = f.readline().split()
    n, m = int(head[0]), int(head[1])
    I = []
    for l in f:
        l = l.split(' ')
        if len(l) < 3: continue
        ntasks = int(l[0])
        I.append([])
        for j in xrange(ntasks):
            mid = int(l[j*2+1])
            dur = int(l[j*2+2])
            I[-1].append((mid, dur))
    return Instance(I, m)


def ComputeDAG(s, I):
    """Compute the DAG representing a solution from a chromosome
    (topological ordering of the DAG)."""
    G = []
    for t in s: G.append([])
    G.append([])
    T = [0 for j in xrange(I.n)]
    last_task_job = [-1 for j in xrange(I.n)]
    tasks_resource = [[-1 for j in xrange(I.n)] for m in xrange(I.m)]
    st = [] # Returns for each task, its id within a job
    for i in xrange(len(s)):
        j = s[i]
        t = T[j]
        st.append(t)
        r = I[j][t][0]
        # If this is the final task of a job, add edge to the final node
        if t + 1 == len(I[j]): G[-1].append(i)
        # Wait for the previous task of the job
        if t > 0: G[i].append(last_task_job[j])
        # Wait for the last task from other jobs using the same resource
        G[i].extend([tasks_resource[r][j2] for j2 in xrange(I.n)
                     if j2 != j and tasks_resource[r][j2] > -1])
        T[j] = T[j] + 1
        last_task_job[j] = i
        tasks_resource[r][j] = i
    return G, st


def ComputeStartTimes(s, I):
    """This computes the start time of each task encoded in a chromosome of
    the genetic algorithm. The last element of the output list is the
    timespan."""
    G, st = ComputeDAG(s, I)
    C = [0 for t in G]
    for i in xrange(len(G)):
        if len(G[i]) == 0: C[i] = 0
        else: C[i] = max(C[k] + I[s[k]][st[k]][1] for k in G[i])
    return C


def FormatSolution(s, C, I):
    T = [0 for j in xrange(I.n)]
    S = [[0 for t in I[j]] for j in xrange(I.n)]
    for i in xrange(len(s)):
        j = s[i]
        t = T[j]
        S[j][t] = C[i]
        T[j] = T[j] + 1
    return S

def Genetic(I, ps = PS, pc = CP, pm = MP, mit = IT):
    def InitPopulation(ps, I):
        """Generate initial population from random shuffles of the tasks."""
        gene = [j for j in xrange(I.n) for t in I[j]]
        population = []
        for i in xrange(ps):
            shuffle(gene)
            population.append([j for j in gene])
        return population

    def Crossover(p1, p2, I):
        """Crossover operation for the GA. Generalized Order Crossover (GOX)."""
        def Index(p1, I):
            ct = [0 for j in xrange(I.n)]
            s = []
            for i in p1:
                s.append((i, ct[i]))
                ct[i] = ct[i] + 1
            return s
        idx_p1 = Index(p1, I)
        idx_p2 = Index(p2, I)
        nt = len(idx_p1) # total number of tasks
        i = randint(1, nt)
        j = randint(0, nt-1)
        k = randint(0, nt)
        implant = idx_p1[j:min(j+i,nt)] + idx_p1[:i - min(j+i,nt) + j]

        lft_child = idx_p2[:k]
        rgt_child = idx_p2[k:]
        for jt in implant:
            if jt in lft_child: lft_child.remove(jt)
            if jt in rgt_child: rgt_child.remove(jt)

        child = [ job for (job, task) in lft_child + implant + rgt_child ]
        return child

    def Mutation(p):
        """Mutation operation for the GA. Swaps to genes of the chromosome."""
        nt = len(p)
        i = randint(0, nt - 1)
        j = randint(0, nt - 1)
        m = [job for job in p]
        m[i], m[j] = m[j], m[i]
        return m

    pop = [(ComputeStartTimes(g, I)[-1], g) for g in InitPopulation(ps, I)]

    best = float('inf')

    for it in xrange(1, mit+1):
        hpop = ELITE
        for i in range(hpop):
            if random() < pc:           
                ch1 = Crossover(pop[i][1], pop[hpop + i][1], I)
                ch2 = Crossover(pop[hpop + i][1], pop[i][1], I)
                if random() < pm:
                    ch1 = Mutation(ch1)
                if random() < pm:
                    ch2 = Mutation(ch2)
                pop.append((ComputeStartTimes(ch1, I)[-1], ch1))
                pop.append((ComputeStartTimes(ch2, I)[-1], ch2))


        # Sort individuals in increasing timespan order and
        # select only the best ones for the next iteration
        pop.sort()
        pop = pop[:ps]
        print(pop[0][0])
    return pop[0]


I = LoadInstance(argv[-1])
(ts, g) = Genetic(I, ps=PS, mit=IT, pc=CP, pm=MP)
