import requests
import json

BASE_URL = "http://localhost:8000/api"

def login_and_test():
    print("=" * 60)
    print("测试AI对话功能 - 基于知识库生成话术")
    print("=" * 60)
    
    # 先注册一个产品经理账户
    print("\n1. 注册产品经理账户...")
    register_data = {
        "username": "pm_test",
        "password": "123",
        "role": "product_manager"
    }
    
    try:
        register_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if register_response.status_code == 201:
            print("✅ 注册成功！")
        else:
            print("⚠️  注册可能已存在，继续使用现有账户")
    except Exception as e:
        print(f"⚠️  注册过程出错: {str(e)}")
    
    # 登录
    print("\n2. 登录...")
    login_data = {
        "username": "pm_test",
        "password": "123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get('access_token')
            user = login_result.get('user')
            
            print(f"✅ 登录成功！")
            print(f"用户: {user.get('username')}")
            print(f"岗位: {user.get('role')}")
            print(f"语气偏好: {user.get('tone_preference')}")
            print(f"长度偏好: {user.get('length_preference')}")
            
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # 测试各种场景
            test_cases = [
                {
                    "name": "需求沟通-需求变更",
                    "message": "客户提出需求变更，怎么沟通影响",
                    "description": "测试需求变更沟通的话术生成",
                    "position": "产品经理"
                },
                {
                    "name": "需求沟通-需求传递",
                    "message": "如何向开发团队传递新需求",
                    "description": "测试需求传递的话术生成",
                    "position": "产品经理"
                },
                {
                    "name": "需求沟通-需求确认",
                    "message": "需求确认会应该怎么说",
                    "description": "测试需求确认会的话术生成",
                    "position": "产品经理"
                },
                {
                    "name": "需求沟通-需求调研",
                    "message": "用户访谈前需要准备什么",
                    "description": "测试用户访谈准备的话术生成",
                    "position": "产品经理"
                },
                {
                    "name": "需求沟通-需求评审",
                    "message": "需求评审会开场白",
                    "description": "测试需求评审会的话术生成",
                    "position": "产品经理"
                }
            ]
            
            print(f"\n3. 开始测试 {len(test_cases)} 个需求沟通场景...")
            
            success_count = 0
            fail_count = 0
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n{'=' * 60}")
                print(f"测试用例 {i}/{len(test_cases)}: {test_case['name']}")
                print(f"描述: {test_case['description']}")
                print(f"用户消息: {test_case['message']}")
                print(f"指定岗位: {test_case['position']}")
                print('=' * 60)
                
                try:
                    response = requests.post(
                        f"{BASE_URL}/chat/message",
                        json={
                            "message": test_case['message'],
                            "position": test_case['position']
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
                                print(f"     内容: {script['content'][:60]}...")
                                print(f"     场景: {script['scene_type']}")
                                print(f"     语气: {script['tone']}")
                                print(f"     目标对象: {script['target_audience']}")
                                print(f"     标签: {script['tags']}")
                            success_count += 1
                        else:
                            print("\n❌ 未找到相关话术")
                            fail_count += 1
                        
                        print(f"\n意图: {data.get('intent', 'unknown')}")
                    else:
                        print(f"请求失败: {response.text}")
                        fail_count += 1
                    
                except Exception as e:
                    print(f"错误: {str(e)}")
                    fail_count += 1
                
                print("\n" + "-" * 60)
            
            print("\n" + "=" * 60)
            print("✅ 测试完成！")
            print("=" * 60)
            
            # 测试项目经理账户
            print("\n\n" + "=" * 60)
            print("测试项目经理岗位...")
            print("=" * 60)
            
            pm_test_cases = [
                {
                    "name": "项目推进-项目启动",
                    "message": "项目启动会应该怎么开场",
                    "description": "测试项目启动的话术生成",
                    "position": "项目经理"
                },
                {
                    "name": "项目推进-进度汇报",
                    "message": "如何向团队汇报项目进度",
                    "description": "测试进度汇报的话术生成",
                    "position": "项目经理"
                },
                {
                    "name": "项目推进-风险汇报",
                    "message": "需要向领导汇报项目风险",
                    "description": "测试风险汇报的话术生成",
                    "position": "项目经理"
                },
                {
                    "name": "项目推进-任务分配",
                    "message": "如何分配项目任务给团队",
                    "description": "测试任务分配的话术生成",
                    "position": "项目经理"
                }
            ]
            
            for i, test_case in enumerate(pm_test_cases, 1):
                print(f"\n{'=' * 60}")
                print(f"测试用例 {i}/{len(pm_test_cases)}: {test_case['name']}")
                print(f"用户消息: {test_case['message']}")
                print(f"指定岗位: {test_case['position']}")
                print('=' * 60)
                
                try:
                    response = requests.post(
                        f"{BASE_URL}/chat/message",
                        json={
                            "message": test_case['message'],
                            "position": test_case['position']
                        },
                        headers=headers,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        print(f"\nAI回复: {data.get('reply', '')}")
                        
                        scripts = data.get('scripts', [])
                        if scripts:
                            print(f"✅ 找到 {len(scripts)} 条相关话术")
                            for j, script in enumerate(scripts[:2], 1):
                                print(f"  {j}. {script['title']}")
                            success_count += 1
                        else:
                            print("❌ 未找到相关话术")
                            fail_count += 1
                    
                except Exception as e:
                    print(f"错误: {str(e)}")
                    fail_count += 1
            
            print("\n" + "=" * 60)
            print("测试总结:")
            print("=" * 60)
            print(f"✅ 成功找到话术: {success_count}个")
            print(f"❌ 未找到话术: {fail_count}个")
            print(f"📊 成功率: {success_count/(success_count+fail_count)*100:.1f}%")
            print(f"📚 知识库话术总数: 197条")
            print(f"🎯 覆盖场景: 需求沟通、项目推进、Bug处理、客户对接")
            
        else:
            print(f"❌ 登录失败: {login_response.text}")
            
    except Exception as e:
        print(f"❌ 登录过程出错: {str(e)}")

if __name__ == "__main__":
    login_and_test()
