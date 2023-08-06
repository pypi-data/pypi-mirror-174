from preamble import * 
 

def reorderingtest(Nx=10,Ny=6,D=2,set_codpy_kernel = kernel_setters.set_gaussian_kernel, rescale = True, seed = 42):
    import random
    print("run test() to start")
    #map_setters.set_min_distance_map()
    if (seed): np.random.seed(seed)
    left = np.random.normal(-3.,1., (int(Nx/2),D))
    right = np.random.normal(3., 1., (int(Nx/2),D))
    x0 = np.concatenate( (left,right) )
    permutation = [i for i in range(0,len(x0))]
    random.shuffle(permutation)
    x0 = x0[permutation]
    y0 = np.random.rand(Ny,D)

    x,y,permutation = alg.reordering(x0,y0, distance ='norm2' )
    reordering_plot(x0,y0,x,y)
    print(x0,y0)
    print(x,y)

    x,y,permutation = alg.reordering(x0,y0, set_codpy_kernel = set_codpy_kernel, rescale = rescale)
    reordering_plot(x0,y0,x,y)

def LSAPtest(Nx=10,Ny=10,set_codpy_kernel = kernel_setters.set_gaussian_kernel, rescale = True, seed = 42, lsap_fun = alg.lsap):
    import random
    print("run test() to start")
    #map_setters.set_min_distance_map()
    if (seed): np.random.seed(seed)
    C = np.random.rand(Nx,Ny)
    cost = np.trace(C).sum()
    print("cost:",cost)
    permutation = lsap_fun(C)
    print("cost:",cost)
    return permutation

def codpy_lsap(C):
    cost = np.trace(C).sum()
    print("cost:",cost)
    permutation = alg.lsap(C)
    cost = np.trace(C[permutation]).sum()
    print("codpy cost:",cost)
    return permutation,cost

def scipy_lsap(C):
    from scipy.optimize import linear_sum_assignment
    N = C.shape[0]
    cost = np.trace(C).sum()
    print("cost:",cost)
    permutation = linear_sum_assignment(C, maximize=False)
    cost = C[permutation[0],permutation[1]].sum()
    out = np.array(range(0,N))
    for n in range(0,N):
        out[permutation[1][n]] = permutation[0][n]
    print("scipy cost:",cost)
    return out, cost
    # cost = np.trace(C[permutation[0]]).sum()

    return permutation[1]
def reordering_plot(x0,y0,x,y,**kwargs):
    from stat_tools import ecdf
    plot_fun = kwargs.get('plot_fun',scatter_plot)
    def helper(x):
        if isinstance(x,list):return [helper(y) for y in x]
        N = len(x)
        out = np.zeros([N,2])
        temp = ecdf(x)
        out[:,0],out[:,1] = temp[0],temp[1]
        return out
    if get_data(x).shape[1] == 1:
        N = len(x)
        x0,y0,x,y = ecdf(x0),ecdf(y0),ecdf(x),ecdf(y)
        multi_plot([( (x0[0], x[0]) , (x0[1],x[1]) ), ( (y0[0], y[0]) , (y0[1],y[1]) ) ],plotD,**kwargs)
    else: multi_plot([(x0,y0),(x,y)],plot_fun,**kwargs)
    plt.show()

if __name__ == "__main__":

    list_results = [(a,b) for a,b in zip(scenario_generator_.accumulator.get_zs(),scenario_generator_.accumulator.get_f_zs())]
    f_names=["linear/periodic no map", "periodic, no map", "gaussian, mean map", "linear regressor, no map"]
    multi_plot(list_results,plot1D,mp_max_items = -1,f_names=f_names, mp_ncols=len(f_names))
    import scipy
    from scipy import stats
    (N,D, df) = (100,2,3)
    xb1 = np.random.normal(-5., 1., (int(N/2),D))
    xb1 = np.concatenate( (xb1,np.random.normal(+5., 1., (int(N/2),D))) )
    xt1 = np.concatenate( (scipy.stats.t.rvs(df, -5., 1.,  (N,D)), scipy.stats.t.rvs(df, 5., 1., (N,D))) )

    M = 30
    yb1 = alg.sampler(xb1,M)
    yt1 = alg.sampler(xt1,M)
    reordering_plot(xb1,yb1,xt1,yt1,f_names=["bi-modal gaussian sampling","bi-modal student sampling"])

   

    def test_seed(seed = 42,N = 4, D=2):
        np.random.seed(seed = seed)
        set_kernel = kernel_setters.kernel_helper(kernel_setters.set_gaussianper_kernel,2,1e-8,None)
        # C = np.random.rand(N,N)
        X = np.random.rand(N,D)
        Y = np.random.rand(N,D)
        C = op.Dnm(X,Y,set_codpy_kernel = set_kernel, rescale = True)
        # C += C.T
        permutation1, cost1 = elapsed_time(lambda **kwargs : codpy_lsap(C))
        permutation2, cost2 = elapsed_time(lambda **kwargs : scipy_lsap(C[permutation1])) 
        if cost2 < cost1:
            print(" cost codpy:",cost1," cost scipy:", cost2)
            np.savetxt("C.txt", C[permutation1],delimiter=';')
    # [test_seed(seed = n, N=4) for n in range(1,1000)]
    reorderingtest()   
    pass 