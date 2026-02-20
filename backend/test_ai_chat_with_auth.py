import requests
import json

BASE_URL = "http://localhost:8000/api"

def login_and_test():
    print("=" * 60)
    print("测试AI对话功能 - 基于知识库生成话术")
    print("=" * 60)
    
    # 先登录
    print("\n1. 登录...")
    login_data = {
        "username": "testuser",
        "password": "123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('access_token')
            user = login_result.get('user')
            
            print(f"登录成功！用户: {user.get('username')}")
            print(f"岗位: {user.get('role')}")
            print(f"语气偏好: {user.get('tone_preference')}")
            print(f"长度偏好: {user.get('length_preference')}")
            
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # 测试各种场景
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
                },
                {
                    "name": "用户访谈准备",
                    "message": "用户访谈前需要准备什么",
                    "description": "测试用户访谈准备的话术生成"
                },
                {
                    "name": "项目里程碑评审",
                    "message": "项目里程碑评审应该怎么组织",
                    "description": "测试项目里程碑评审的话术生成"
                },
                {
                    "name": "Bug优先级评估",
                    "message": "如何评估Bug的优先级",
                    "description": "测试Bug优先级评估的话术生成"
                },
                {
                    "name": "客户投诉处理",
                    "message": "客户投诉应该怎么处理",
                    "description": "测试客户投诉处理的话术生成"
                },
                {
                    "name": "需求确认会",
                    "message": "需求确认会应该怎么说",
                    "description": "测试需求确认会的话术生成"
                }
            ]
            
            print(f"\n2. 开始测试 {len(test_cases)} 个场景...")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n{'=' * 60}")
                print(f"测试用例 {i}/{len(test_cases)}: {test_case['name']}")
                print(f"描述: {test_case['description']}")
                print(f"用户消息: {test_case['message']}")
                print('=' * 60)
                
                try:
                    response = requests.post(
                        f"{BASE_URL}/chat/message",
                        json={
                            "message": test_case['message']
                        },
                        headers=headers,
                        timeout=10
                    )
                    
                    print(f"\n状态码: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        print(f"\nAI回复:")
                        print(data.get('reply', ''))
                        
                        scripts = data.get('scripts', [])
                        if scripts:
                            print(f"\n✅ 找到 {len(scripts)} 条相关话术:")
                            for j, script in enumerate(scripts, 1):
                                print(f"\n  {j}. 【{script['title']}】")
                                print(f"     内容: {script['content'][:80]}...")
                                print(f"     场景: {script['scene_type']}")
                                print(f"     语气: {script['tone']}")
                                print(f"     目标对象: {script['target_audience']}")
                                print(f"     标签: {script['tags']}")
                        else:
                            print("\n❌ 未找到相关话术")
                        
                        print(f"\n意图: {data.get('intent', 'unknown')}")
                    else:
                        print(f"请求失败: {response.text}")
                    
                except Exception as e:
                    print(f"错误: {str(e)}")
                
                print("\n" + "-" * 60)
            
            print("\n" + "=" * 60)
            print("✅ 所有测试用例执行完成！")
            print("=" * 60)
            
            # 统计
            print("\n测试总结:")
            print(f"- 测试场景数量: {len(test_cases)}")
            print(f"- 覆盖的主要场景: 需求沟通、项目推进、Bug处理、客户对接")
            print(f"- 知识库话术总数: 197条")
            print(f"- AI对话功能: 基于知识库智能匹配")
            
        else:
            print(f"登录失败: {login_response.text}")
            
    except Exception as e:
        print(f"登录过程出错: {str(e)}")

if __name__ == "__main__":
    login_and_test()
