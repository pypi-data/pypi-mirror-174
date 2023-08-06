.. currentmodule:: calplot


Calendar heatmaps from Pandas time series data
==============================================

Plot `Pandas <http://pandas.pydata.org/>`_ time series data sampled by day in
a heatmap per calendar year, similar to GitHub's contributions plot, using
`matplotlib <http://matplotlib.org/>`_.

Package `calplot <https://pypi.org/project/calplot/>`_ was started as a fork of `calmap <https://github.com/martijnvermaat/calmap>`_ with the addition of new arguments for easier customization of plots. Code refactoring was carried out to increase the maintainability of this package.

Installation
------------

To install the latest release via PyPI using pip::

    pip install calplot

The latest development version `can be found on GitHub
<https://github.com/tomkwok/calplot>`_.

Usage
-----

Assume we have some weighted events as a Pandas Series with a
DatetimeIndex.

For illustration purposes we just create 500 events as random float values
assigned to random days over a 730-day period:

.. plot::
    :context: close-figs

    import numpy as np; np.random.seed(sum(map(ord, 'calplot')))
    import pandas as pd
    import calplot

    all_days = pd.date_range('1/1/2019', periods=730, freq='D')
    days = np.random.choice(all_days, 500)
    events = pd.Series(np.random.randn(len(days)), index=days)

We can use :func:`calplot` to plot all years as subplots into one
figure:

.. plot::
    :context: close-figs

    calplot.calplot(events, cmap='YlGn', colorbar=False)

.. _api:

In particular, note that :code:`calplot.calplot()` wraps :code:`calplot.yearplot()`. Keyword arguments passed to :code:`calplot.calplot()` will be passed to :code:`calplot.yearplot()` when it is called.

API documentation
-----------------

.. module:: calplot
.. autofunction:: yearplot
.. autofunction:: calplot


Copyright
---------

This library is licensed under the MIT License, meaning you can do whatever
you want with it as long as all copies include these license terms. The full
license text can be found in the LICENSE.rst file. See the AUTHORS.rst for for
a complete list of copyright holders.
