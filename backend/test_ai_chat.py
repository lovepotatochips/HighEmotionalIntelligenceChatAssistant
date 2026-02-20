import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_ai_chat():
    print("=" * 60)
    print("测试AI对话功能 - 基于知识库生成话术")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "需求沟通场景",
            "message": "我需要向产品经理反馈一个需求变更的问题",
            "description": "测试需求沟通场景的话术生成"
        },
        {
            "name": "项目推进场景",
            "message": "项目进度滞后了，我需要向团队催促进度",
            "description": "测试项目推进场景的话术生成"
        },
        {
            "name": "Bug处理场景",
            "message": "发现了一个严重的Bug，需要反馈给后端开发",
            "description": "测试Bug处理场景的话术生成"
        },
        {
            "name": "客户对接场景",
            "message": "客户对我们的价格有异议，我需要处理",
            "description": "测试客户对接场景的话术生成"
        },
        {
            "name": "需求调研",
            "message": "如何进行用户访谈，了解用户需求",
            "description": "测试需求调研的话术生成"
        },
        {
            "name": "项目启动",
            "message": "项目启动会应该怎么开场",
            "description": "测试项目启动的话术生成"
        },
        {
            "name": "Bug提交",
            "message": "怎么向开发团队提交Bug",
            "description": "测试Bug提交流程的话术生成"
        },
        {
            "name": "客户接待",
            "message": "初次接待客户应该怎么说",
            "description": "测试客户接待的话术生成"
        },
        {
            "name": "需求变更沟通",
            "message": "客户提出需求变更，怎么沟通影响",
            "description": "测试需求变更沟通的话术生成"
        },
        {
            "name": "项目风险汇报",
            "message": "需要向领导汇报项目风险",
            "description": "测试项目风险汇报的话术生成"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"测试用例 {i}: {test_case['name']}")
        print(f"描述: {test_case['description']}")
        print(f"用户消息: {test_case['message']}")
        print('=' * 60)
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat/message",
                json={
                    "message": test_case['message']
                },
                timeout=10
            )
            
            print(f"\n状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"\nAI回复:")
                print(data.get('reply', ''))
                
                scripts = data.get('scripts', [])
                if scripts:
                    print(f"\n找到 {len(scripts)} 条相关话术:")
                    for j, script in enumerate(scripts, 1):
                        print(f"\n{j}. {script['title']}")
                        print(f"   内容: {script['content'][:100]}...")
                        print(f"   场景: {script['scene_type']}")
                        print(f"   语气: {script['tone']}")
                        print(f"   标签: {script['tags']}")
                else:
                    print("\n未找到相关话术")
                
                print(f"\n意图: {data.get('intent', 'unknown')}")
            else:
                print(f"请求失败: {response.text}")
                
        except Exception as e:
            print(f"错误: {str(e)}")
        
        print("\n" + "-" * 60)
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_ai_chat()
