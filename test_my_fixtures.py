import pathlib
import pytest


@pytest.fixture
def read_conftest(request):
    return pathlib.Path(request.config.rootdir, 'conftest.py').read_text()


def test_my_fixture(testdir, read_conftest):
    testdir.makeconftest(read_conftest)
    testdir.makepyfile(
        """
          import os  
          import pytest
          
          AUTOUSE = "autouse.txt"
          FUNCTION = "function.txt"
          CLASS = "class.txt"
          MODULE = "module.txt"
          SESSION = "session.txt"
      
          @pytest.fixture(autouse=True)
          def i_am_autouse():
              f = open(AUTOUSE, "w")
              f.close()
              yield
              os.remove(AUTOUSE)
      
          @pytest.fixture(scope="function")
          def i_am_function():
              f = open(FUNCTION, "w")
              f.close()
              yield
              os.remove(FUNCTION)
      
          @pytest.fixture(scope="class")
          def i_am_class():
              f = open(CLASS, "w")
              f.close()
              yield
              os.remove(CLASS)
              
          @pytest.fixture(scope="module")
          def i_am_module():
              f = open(MODULE, "w")
              f.close()
              yield
              os.remove(MODULE)
              
          @pytest.fixture(scope="session")
          def i_am_session():
              f = open(SESSION, "w")
              f.close()
              yield
              os.remove(SESSION)
      
          class TestOne:
               
              def test_autouse_fixture(self):
                  assert os.path.isfile(AUTOUSE)
              
              @pytest.mark.usefixtures("i_am_function")    
              def test_function_level_fixture(self):
                  assert os.path.isfile(FUNCTION)
              
              @pytest.mark.usefixtures("i_am_class")    
              def test_class_level_fixture(self):
                  assert os.path.isfile(CLASS)
                  
              def test_class_level_fixture_same_class(self):
                  assert os.path.isfile(CLASS)
              
              @pytest.mark.usefixtures("i_am_module")    
              def test_module_level_fixture(self):
                  assert os.path.isfile(MODULE)  
           
          class TestTwo: 
              def test_autouse_fixture_different_class(self):
                  assert os.path.isfile(AUTOUSE)
          
              def test_class_fixture_different_class(self):
                  assert not os.path.isfile(CLASS)
              
              def test_module_fixture_on_class_level(self):
                  assert os.path.isfile(MODULE)
                  
          def test_class_fixture_on_module_level():
              assert not os.path.isfile(CLASS)
              
          def test_module_fixture_on_module_level():
              assert os.path.isfile(MODULE)
             
          @pytest.mark.usefixtures("i_am_session")
          def test_session_fixture_on_module_level():
              assert os.path.isfile(SESSION)
              
          def test_function_level_fixture_when_not_called():
              assert not os.path.isfile(FUNCTION)
            """
    )
    result = testdir.runpytest()
    result.assert_outcomes(passed=12)
