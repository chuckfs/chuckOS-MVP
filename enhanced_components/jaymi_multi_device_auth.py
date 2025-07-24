#!/usr/bin/env python3
# /usr/local/bin/jaymi_multi_device_auth.py

import asyncio
import json
import hashlib
import time
import uuid
import usb.core
import usb.util
import bluetooth
import subprocess
import threading
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
import hmac
import qrcode
import io
import base64
import secrets  # Used but not imported

class DeviceType(Enum):
    USB_KEY = "usb_key"
    SMARTPHONE = "smartphone" 
    LAPTOP = "laptop"
    HARDWARE_KEY = "hardware_key"
    BIOMETRIC = "biometric"

class AuthStatus(Enum):
    PENDING = "pending"
    AUTHENTICATED = "authenticated"
    FAILED = "failed"
    TIMEOUT = "timeout"

@dataclass
class DeviceSignature:
    device_id: str
    device_type: DeviceType
    device_name: str
    public_key: str
    fingerprint: str
    last_seen: float
    trust_level: float  # 0.0 to 1.0
    metadata: Dict[str, Any]

@dataclass
class AuthAttempt:
    attempt_id: str
    timestamp: float
    devices_required: int
    devices_authenticated: List[str]
    status: AuthStatus
    timeout_seconds: int
    challenge: str

class MultiDeviceAuthManager:
    """Advanced 3-device authentication system"""
    
    def __init__(self, vault_path: str = "/.chuck_secure"):
        self.vault_path = Path(vault_path)
        self.auth_config_path = self.vault_path / "auth_config.json"
        self.devices_path = self.vault_path / "devices.json"
        self.auth_log_path = self.vault_path / "auth_log.json"
        
        # Authentication settings
        self.required_devices = 3
        self.auth_timeout = 300  # 5 minutes
        self.challenge_length = 32
        
        # Current authentication state
        self.registered_devices: Dict[str, DeviceSignature] = {}
        self.current_attempt: Optional[AuthAttempt] = None
        self.authenticated_devices: Dict[str, float] = {}  # device_id -> timestamp
        
        # Background scanning
        self.scanning_active = False
        self.scan_interval = 2.0  # seconds
        
        # Initialize
        self._load_configuration()
        self._load_registered_devices()
    
    def _load_configuration(self):
        """Load authentication configuration"""
        if self.auth_config_path.exists():
            try:
                with open(self.auth_config_path) as f:
                    config = json.load(f)
                    self.required_devices = config.get("required_devices", 3)
                    self.auth_timeout = config.get("auth_timeout", 300)
            except Exception as e:
                print(f"❌ Failed to load auth config: {e}")
    
    def _load_registered_devices(self):
        """Load registered device signatures"""
        if self.devices_path.exists():
            try:
                with open(self.devices_path) as f:
                    devices_data = json.load(f)
                    self.registered_devices = {
                        device_id: DeviceSignature(**device_data)
                        for device_id, device_data in devices_data.items()
                    }
                print(f"📱 Loaded {len(self.registered_devices)} registered devices")
            except Exception as e:
                print(f"❌ Failed to load devices: {e}")
    
    def _save_registered_devices(self):
        """Save registered device signatures"""
        try:
            devices_data = {
                device_id: asdict(device)
                for device_id, device in self.registered_devices.items()
            }
            with open(self.devices_path, 'w') as f:
                json.dump(devices_data, f, indent=2)
        except Exception as e:
            print(f"❌ Failed to save devices: {e}")
    
    async def start_device_scanning(self):
        """Start background device scanning"""
        if not self.scanning_active:
            self.scanning_active = True
            asyncio.create_task(self._device_scan_loop())
            print("🔍 Device scanning started")
    
    async def stop_device_scanning(self):
        """Stop background device scanning"""
        self.scanning_active = False
        print("🛑 Device scanning stopped")
    
    async def register_new_device(self, device_type: DeviceType, 
                                device_name: str) -> Tuple[bool, str]:
        """Register a new authentication device"""
        
        print(f"📝 Registering new {device_type.value}: {device_name}")
        
        if device_type == DeviceType.USB_KEY:
            return await self._register_usb_device(device_name)
        elif device_type == DeviceType.SMARTPHONE:
            return await self._register_smartphone(device_name)
        elif device_type == DeviceType.LAPTOP:
            return await self._register_laptop(device_name)
        elif device_type == DeviceType.HARDWARE_KEY:
            return await self._register_hardware_key(device_name)
        else:
            return False, f"Unsupported device type: {device_type.value}"
    
    async def _register_usb_device(self, device_name: str) -> Tuple[bool, str]:
        """Register USB device for authentication"""
        
        print("🔌 Please insert USB device to register...")
        
        # Wait for USB device insertion
        timeout = 30  # 30 seconds
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            devices = usb.core.find(find_all=True)
            for device in devices:
                try:
                    # Get device info
                    device_info = {
                        "vendor_id": device.idVendor,
                        "product_id": device.idProduct,
                        "serial": device.serial_number if hasattr(device, 'serial_number') else None
                    }
                    
                    # Generate device fingerprint
                    fingerprint_data = f"{device_info['vendor_id']}:{device_info['product_id']}:{device_info['serial']}"
                    fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
                    
                    # Check if already registered
                    if any(dev.fingerprint == fingerprint for dev in self.registered_devices.values()):
                        continue
                    
                    # Generate device ID and keys
                    device_id = str(uuid.uuid4())
                    public_key = self._generate_device_keys(device_id)
                    
                    # Create device signature
                    device_sig = DeviceSignature(
                        device_id=device_id,
                        device_type=DeviceType.USB_KEY,
                        device_name=device_name,
                        public_key=public_key,
                        fingerprint=fingerprint,
                        last_seen=time.time(),
                        trust_level=1.0,
                        metadata=device_info
                    )
                    
                    # Register device
                    self.registered_devices[device_id] = device_sig
                    self._save_registered_devices()
                    
                    print(f"✅ USB device registered: {device_name}")
                    return True, f"Device registered with ID: {device_id}"
                    
                except Exception as e:
                    continue
            
            await asyncio.sleep(1)
        
        return False, "Timeout waiting for USB device"
    
    async def _register_smartphone(self, device_name: str) -> Tuple[bool, str]:
        """Register smartphone via QR code pairing"""
        
        # Generate pairing challenge
        challenge = secrets.token_urlsafe(32)
        device_id = str(uuid.uuid4())
        
        # Create pairing QR code
        pairing_data = {
            "device_id": device_id,
            "challenge": challenge,
            "timestamp": time.time(),
            "auth_endpoint": "http://localhost:8080/pair"
        }
        
        qr_data = json.dumps(pairing_data)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Display QR code (simplified - in real implementation would show in terminal)
        print(f"📱 Scan this QR code with your smartphone:")
        print(f"QR Data: {qr_data}")
        
        # Wait for pairing confirmation
        timeout = 120  # 2 minutes
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Check for pairing file (smartphone app would create this)
            pairing_file = Path(f"/tmp/jaymi_pair_{device_id}.json")
            if pairing_file.exists():
                try:
                    with open(pairing_file) as f:
                        pair_response = json.load(f)
                    
                    # Verify challenge response
                    if pair_response.get("challenge") == challenge:
                        # Create device signature
                        device_sig = DeviceSignature(
                            device_id=device_id,
                            device_type=DeviceType.SMARTPHONE,
                            device_name=device_name,
                            public_key=pair_response.get("public_key", ""),
                            fingerprint=pair_response.get("fingerprint", ""),
                            last_seen=time.time(),
                            trust_level=0.9,
                            metadata=pair_response.get("metadata", {})
                        )
                        
                        self.registered_devices[device_id] = device_sig
                        self._save_registered_devices()
                        
                        # Clean up pairing file
                        pairing_file.unlink()
                        
                        print(f"✅ Smartphone registered: {device_name}")
                        return True, f"Device registered with ID: {device_id}"
                
                except Exception as e:
                    print(f"❌ Pairing error: {e}")
            
            await asyncio.sleep(2)
        
        return False, "Pairing timeout"
    
    async def _register_laptop(self, device_name: str) -> Tuple[bool, str]:
        """Register secondary laptop via network"""
        
        # Get current machine fingerprint
        fingerprint = self._get_machine_fingerprint()
        device_id = str(uuid.uuid4())
        public_key = self._generate_device_keys(device_id)
        
        # Create device signature
        device_sig = DeviceSignature(
            device_id=device_id,
            device_type=DeviceType.LAPTOP,
            device_name=device_name,
            public_key=public_key,
            fingerprint=fingerprint,
            last_seen=time.time(),
            trust_level=0.8,
            metadata={"hostname": subprocess.getoutput("hostname")}
        )
        
        self.registered_devices[device_id] = device_sig
        self._save_registered_devices()
        
        print(f"✅ Laptop registered: {device_name}")
        return True, f"Device registered with ID: {device_id}"
    
    async def begin_authentication(self) -> str:
        """Begin multi-device authentication process"""
        
        if len(self.registered_devices) < self.required_devices:
            raise ValueError(f"Need {self.required_devices} devices, only {len(self.registered_devices)} registered")
        
        # Create authentication attempt
        attempt_id = str(uuid.uuid4())
        challenge = secrets.token_urlsafe(self.challenge_length)
        
        self.current_attempt = AuthAttempt(
            attempt_id=attempt_id,
            timestamp=time.time(),
            devices_required=self.required_devices,
            devices_authenticated=[],
            status=AuthStatus.PENDING,
            timeout_seconds=self.auth_timeout,
            challenge=challenge
        )
        
        # Start authentication timeout
        asyncio.create_task(self._authentication_timeout())
        
        print(f"🔐 Authentication started - need {self.required_devices} devices")
        print(f"⏰ Timeout in {self.auth_timeout} seconds")
        
        return attempt_id
    
    async def authenticate_device(self, device_id: str, 
                                signature: str) -> Tuple[bool, str]:
        """Authenticate a specific device"""
        
        if not self.current_attempt:
            return False, "No authentication in progress"
        
        if self.current_attempt.status != AuthStatus.PENDING:
            return False, "Authentication not in pending state"
        
        if device_id not in self.registered_devices:
            return False, "Device not registered"
        
        if device_id in self.current_attempt.devices_authenticated:
            return False, "Device already authenticated"
        
        # Verify device signature
        device = self.registered_devices[device_id]
        if self._verify_device_signature(device, signature, self.current_attempt.challenge):
            # Add to authenticated devices
            self.current_attempt.devices_authenticated.append(device_id)
            self.authenticated_devices[device_id] = time.time()
            
            print(f"✅ Device authenticated: {device.device_name}")
            print(f"📊 Progress: {len(self.current_attempt.devices_authenticated)}/{self.required_devices}")
            
            # Check if authentication complete
            if len(self.current_attempt.devices_authenticated) >= self.required_devices:
                self.current_attempt.status = AuthStatus.AUTHENTICATED
                await self._log_auth_attempt(success=True)
                print("🎉 Multi-device authentication successful!")
                return True, "Authentication complete"
            
            return True, f"Device authenticated ({len(self.current_attempt.devices_authenticated)}/{self.required_devices})"
        
        else:
            await self._log_auth_attempt(success=False, device_id=device_id)
            return False, "Invalid device signature"
    
    async def _device_scan_loop(self):
        """Background loop for detecting authentication devices"""
        
        while self.scanning_active:
            try:
                # Scan for USB devices
                await self._scan_usb_devices()
                
                # Scan for Bluetooth devices
                await self._scan_bluetooth_devices()
                
                # Check for network devices
                await self._scan_network_devices()
                
                await asyncio.sleep(self.scan_interval)
                
            except Exception as e:
                print(f"Device scan error: {e}")
                await asyncio.sleep(self.scan_interval)
    
    async def _scan_usb_devices(self):
        """Scan for registered USB devices"""
        
        if not self.current_attempt or self.current_attempt.status != AuthStatus.PENDING:
            return
        
        devices = usb.core.find(find_all=True)
        for device in devices:
            try:
                # Generate fingerprint
                device_info = {
                    "vendor_id": device.idVendor,
                    "product_id": device.idProduct,
                    "serial": getattr(device, 'serial_number', None)
                }
                
                fingerprint_data = f"{device_info['vendor_id']}:{device_info['product_id']}:{device_info['serial']}"
                fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
                
                # Check if registered
                for device_id, registered_device in self.registered_devices.items():
                    if (registered_device.fingerprint == fingerprint and 
                        registered_device.device_type == DeviceType.USB_KEY and
                        device_id not in self.current_attempt.devices_authenticated):
                        
                        # Auto-authenticate USB device
                        signature = self._generate_device_signature(registered_device, self.current_attempt.challenge)
                        await self.authenticate_device(device_id, signature)
                        
            except Exception:
                continue
    
    def _verify_device_signature(self, device: DeviceSignature, 
                                signature: str, challenge: str) -> bool:
        """Verify device signature against challenge"""
        
        # Create expected signature
        signature_data = f"{device.device_id}:{challenge}:{device.fingerprint}"
        expected_signature = hmac.new(
            device.public_key.encode(),
            signature_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def _generate_device_signature(self, device: DeviceSignature, challenge: str) -> str:
        """Generate signature for device authentication"""
        
        signature_data = f"{device.device_id}:{challenge}:{device.fingerprint}"
        return hmac.new(
            device.public_key.encode(),
            signature_data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _generate_device_keys(self, device_id: str) -> str:
        """Generate cryptographic keys for device"""
        
        # Generate a device-specific key
        key_material = f"{device_id}:{time.time()}:{secrets.token_hex(32)}"
        return hashlib.sha256(key_material.encode()).hexdigest()
    
    def _get_machine_fingerprint(self) -> str:
        """Get unique machine fingerprint"""
        
        try:
            # Combine multiple system identifiers
            machine_id = subprocess.getoutput("cat /etc/machine-id").strip()
            cpu_info = subprocess.getoutput("cat /proc/cpuinfo | grep 'model name' | head -1").strip()
            hostname = subprocess.getoutput("hostname").strip()
            
            fingerprint_data = f"{machine_id}:{cpu_info}:{hostname}"
            return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
        except:
            # Fallback fingerprint
            import platform
            fallback_data = f"{platform.node()}:{platform.processor()}:{platform.system()}"
            return hashlib.sha256(fallback_data.encode()).hexdigest()[:16]
    
    async def _authentication_timeout(self):
        """Handle authentication timeout"""
        
        await asyncio.sleep(self.auth_timeout)
        
        if self.current_attempt and self.current_attempt.status == AuthStatus.PENDING:
            self.current_attempt.status = AuthStatus.TIMEOUT
            await self._log_auth_attempt(success=False, reason="timeout")
            print("⏰ Authentication timed out")
    
    async def _log_auth_attempt(self, success: bool, device_id: str = None, reason: str = None):
        """Log authentication attempt"""
        
        log_entry = {
            "timestamp": time.time(),
            "attempt_id": self.current_attempt.attempt_id if self.current_attempt else "unknown",
            "success": success,
            "devices_authenticated": len(self.current_attempt.devices_authenticated) if self.current_attempt else 0,
            "device_id": device_id,
            "reason": reason
        }
        
        try:
            # Load existing log
            if self.auth_log_path.exists():
                with open(self.auth_log_path) as f:
                    log_data = json.load(f)
            else:
                log_data = []
            
            # Add new entry
            log_data.append(log_entry)
            
            # Keep only recent entries (last 1000)
            if len(log_data) > 1000:
                log_data = log_data[-1000:]
            
            # Save log
            with open(self.auth_log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"Failed to log auth attempt: {e}")
    
    def get_authentication_status(self) -> Dict[str, Any]:
        """Get current authentication status"""
        
        if not self.current_attempt:
            return {"status": "no_authentication", "authenticated_devices": 0}
        
        return {
            "status": self.current_attempt.status.value,
            "attempt_id": self.current_attempt.attempt_id,
            "devices_required": self.required_devices,
            "devices_authenticated": len(self.current_attempt.devices_authenticated),
            "authenticated_device_names": [
                self.registered_devices[device_id].device_name
                for device_id in self.current_attempt.devices_authenticated
            ],
            "time_remaining": max(0, self.auth_timeout - (time.time() - self.current_attempt.timestamp))
        }
    
    def list_registered_devices(self) -> List[Dict[str, Any]]:
        """List all registered devices"""
        
        return [
            {
                "device_id": device.device_id,
                "device_type": device.device_type.value,
                "device_name": device.device_name,
                "fingerprint": device.fingerprint[:8] + "...",
                "last_seen": device.last_seen,
                "trust_level": device.trust_level
            }
            for device in self.registered_devices.values()
        ]

# Global auth manager instance
auth_manager = MultiDeviceAuthManager()
