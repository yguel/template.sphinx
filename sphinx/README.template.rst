=============================
Quick install and test setup
=============================

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   sphinx-build -b html -D language=en ./source ./build/html/%(VERSION_NAME)s/en

To see the result, open the file `build/html/%(VERSION_NAME)s/en/index.html` in your browser.

.. code-block:: bash

   # To see the result, open the file
   firefox build/html/%(VERSION_NAME)s/en/index.html

=================================
First time for translation setup
=================================

.. code-block:: bash

    # Create gettext files
    make gettext

    # Update gettext files
    sphinx-build -b gettext source build/gettext

    # Update all po files
    sphinx-intl update -p build/gettext -d source/locales


==================================
Update translation files
==================================

.. code-block:: bash

    # Update gettext files
    sphinx-build -b gettext source build/gettext

    # Update all po files
    sphinx-intl update -p build/gettext -d source/locales

    ## Eventually see errors (otherwise it will silently fail)
    ### to be done for each pot file
    msgmerge --update source/locales/en/LC_MESSAGES/c00_setup_de_ros2/c00s01_ros2_setup.po build/gettext/c00_setup_de_ros2/c00s01_ros2_setup.pot


Then you have to add the translations in the `source/locales/en_US/LC_MESSAGES/*.po` files.
Then you can build the html files with the following command corresponding to the language you want to build.

.. code-block:: bash

   # Check the po files for errors only
   find source/locales/ -iname "*.po" | xargs -n1 msgfmt --check 2>&1 | grep -v "warning"
   # Check the po files for errors and warnings
   find source/locales/ -iname "*.po" | xargs -n1 msgfmt --check

.. code-block:: bash
   
    # Build html files for the language en in html/en
    sphinx-build -b html -D language=fr ./source ./build/html/%(VERSION_NAME)s/fr
    sphinx-build -b html -D language=en ./source ./build/html/%(VERSION_NAME)s/en