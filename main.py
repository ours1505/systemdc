#!/bin/env python3
import os
import subprocess
import sys

class SystemdManager:
    def __init__(self):
        # Check if running as root
        if os.geteuid() != 0:
            print("请使用root权限运行此脚本")
            sys.exit(1)
            
        self.service_dir: str = "/etc/systemd/system"

    def create_service(self, name: str, exec_path: str, description: str = "", restart: str = "always", working_dir: str = "") -> bool:
        """
        Create a new systemd service
        name: Service name
        exec_path: Path to executable
        description: Service description
        restart: Restart policy (always/on-failure/no)
        working_dir: Working directory for the service
        """
        # Add input validation
        if not name or not exec_path:
            print("错误：服务名称和可执行文件路径不能为空")
            return False
        
        # Check if service already exists
        service_file = f"{self.service_dir}/{name}.service"
        if os.path.exists(service_file):
            print(f"错误：服务 {name} 已存在")
            return False
        
        # Check only the first part of the command if it's a command string
        command_parts = exec_path.split()
        if not os.path.exists(command_parts[0]):
            # Try to find the executable in PATH
            command_path = subprocess.run(['which', command_parts[0]], capture_output=True, text=True).stdout.strip()
            if not command_path:
                print(f"警告：命令 {command_parts[0]} 在系统中未找到，但仍将继续创建服务")

        service_content = f"""[Unit]
Description={description}

[Service]
Type=simple
ExecStart={exec_path}
Restart={restart}
RestartSec=5
{f'WorkingDirectory={working_dir}' if working_dir else ''}

[Install]
WantedBy=multi-user.target
"""
        
        try:
            with open(service_file, "w") as f:
                f.write(service_content)
            
            print(f"服务 {name} 创建成功")
            
            # Add error handling for systemctl commands
            try:
                subprocess.run(["systemctl", "daemon-reload"], check=True)
                subprocess.run(["systemctl", "enable", name], check=True)
                subprocess.run(["systemctl", "start", name], check=True)
                print(f"服务已启用并启动，可使用 'systemctl status {name}' 查看状态")
            except subprocess.CalledProcessError as e:
                print(f"警告：服务文件已创建，但启动服务时出错: {str(e)}")
            
            return True
            
        except Exception as e:
            print(f"创建服务失败: {str(e)}")
            return False

def main():
    """Interactive mode for creating systemd service"""
    print("欢迎使用 Systemd 服务创建工具")
    print("-" * 40)
    
    # Add input validation
    while True:
        name = input("请输入服务名称: ").strip()
        # Allow letters, numbers, hyphen, at sign, and underscore
        if name and all(c.isalnum() or c in '-@_' for c in name):
            break
        print("错误：服务名称不能为空且只能包含字母、数字、连字符(-)、@符号和下划线(_)")
    description = input("请输入服务描述 (可选): ").strip()
    
    while True:
        exec_path = input("执行命令: ").strip()
        if exec_path:
            break
        print("错误：命令不能为空")
    working_dir = input("请输入工作目录 (可选): ").strip()
    
    
    # Restart policy selection
    print("\n请选择重启策略:")
    print("1. always (总是重启)")
    print("2. on-failure (仅在失败时重启)")
    print("3. no (不自动重启)")
    
    while True:
        choice = input("请输入选项 (1-3) [默认: 1]: ").strip()
        if choice == "" or choice == "1":
            restart = "always"
            break
        elif choice == "2":
            restart = "on-failure"
            break
        elif choice == "3":
            restart = "no"
            break
        else:
            print("无效的选项，请重新输入")
    
    
    
    # Create service
    manager = SystemdManager()
    _ = manager.create_service(
        name=name,
        exec_path=exec_path,
        description=description,
        restart=restart,
        working_dir=working_dir
    )

if __name__ == "__main__":
    main()


