import numpy as np

seconds = 10
sample_rate = 128
time = np.linspace(0,seconds,seconds*sample_rate)
x = np.sin(2*np.pi*5*time)

def _third_order_cumulant(x, maxlag=200):
    """Pretty slow atm, must be a faster way - numba perhaps?"""

    lags = np.arange(-maxlag,maxlag)
    toc = np.zeros((len(lags),len(lags)))
    for ii in range(len(lags)):
        for jj in range(len(lags)):
            base_start = -lags[0]
            base_stop = x.shape[0]-lags[-1]
            x0 = x[base_start:base_stop]
            x1 = x[base_start+lags[ii]:base_stop+lags[ii]]
            x2 = x[base_start+lags[jj]:base_stop+lags[jj]]
            toc[ii,jj] = np.mean(x0*x1*x2)
    return toc

def bispectrum(x, sample_rate, maxlag=None):

    if maxlag is None:
        maxlag = x.shape[0]//2

    toc = _third_order_cumulant(x, maxlag=maxlag)

    bispec = np.fft.fftshift(np.fft.fft2(toc))
    freq = np.fft.fftshift(np.fft.fftfreq(toc.shape[0],1/sample_rate))

    return bispec, freq

bis,f = bispectrum(x,sample_rate)
bis2,f = bispectrum(x2,sample_rate)

plt.figure()
plt.subplot(121)
contourf(f,f,np.abs(bis))
xlim(0,30); ylim(0,30)
plt.subplot(122)
contourf(f,f,np.abs(bis2))
xlim(0,30); ylim(0,30)
