pip3 -V
(if [ -d local_lib ]; then
   rm -rf local_lib
fi
pip3 install --target local_lib git+https://github.com/jaraco/path.git > install.log 2>&1)
if [ $? -eq 0 ]; then python3 my_program.py
fi
