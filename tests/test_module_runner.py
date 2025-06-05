import sys
from unittest.mock import MagicMock, patch

from concurrent_modular_agent import module_main, AgentInterface
from concurrent_modular_agent.agent_runner import find_module_main_function

### 1. `find_module_main_function` のテスト
def test_find_module_main_function():
    script_path = "/fake/script.py"
    
    # 模擬モジュールを作成
    mock_module = type(sys)("mock_module")
    
    # デコレータを適用した関数を定義
    @module_main("fake_main2")
    def fake_main(agent):
        pass
        # print("#######")
    
    mock_module.fake_main = fake_main

    # `importlib` のモック
    with patch("importlib.util.spec_from_file_location") as mock_spec, \
         patch("importlib.util.module_from_spec", return_value=mock_module) as mock_mod, \
         patch("sys.modules", {"module.name": mock_module}):
        
        mock_loader = MagicMock()
        mock_loader.exec_module = MagicMock()
        mock_spec.return_value.loader = mock_loader
        
        main_func = find_module_main_function(script_path)
        assert main_func == fake_main
        # import ipdb; ipdb.set_trace()
        # main_func()
        

@module_main("fake_main1")
def fake_main(agent):
    isinstance(agent, AgentInterface)

def test_find_module_main_function_2():
    main_func = find_module_main_function(__file__)
    assert main_func is not None
    assert main_func.__name__ == 'fake_main'
    main_func()