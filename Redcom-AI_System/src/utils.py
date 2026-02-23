import pandas as pd
import numpy as np

def preprocess_data_app(df: pd.DataFrame):
    df = df.copy()
    
    # Cleaning column names (preventing issues with trailing spaces)
    df.columns = df.columns.str.strip()
    
    # Removing forbidden columns according to the guidelines
    drop_cols = [
        'Source_IP', 'Destination_IP', 'Source_port', 'Destination_port', 
        'Timestamp', 'label', 'attribution', 'prediction'
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    
    # Protocol encoding
    if 'Protocol' in df.columns:
        df['Protocol'] = df['Protocol'].map({'tcp': 6, 'udp': 17}).fillna(0)
        
    # --- Advanced feature engineering to compensate for the lack of ports ---
    # 1. Packet ratio (incoming/outgoing)
    if 'fwd_packets_amount' in df.columns and 'bwd_packets_amount' in df.columns:
        df['packets_ratio'] = df['fwd_packets_amount'] / (df['bwd_packets_amount'] + 1)
        
    # 2. Data size ratio (Bytes)
    if 'fwd_packets_length' in df.columns and 'bwd_packets_length' in df.columns:
        df['bytes_ratio'] = df['fwd_packets_length'] / (df['bwd_packets_length'] + 1)
        
    # 3. Average data density
    if 'mean_packet_size' in df.columns:
        df['large_packet_flag'] = (df['mean_packet_size'] > 500).astype(int)

    # Keeping only numeric columns and handling missing/infinite values
    df = df.select_dtypes(include=['number'])
    df = df.replace([np.inf, -np.inf], 0).fillna(0)
    
    return df

def preprocess_data_att(df: pd.DataFrame):
    df = df.copy()
    
    # We remove IPs, Ports, and Timestamps to avoid Overfitting.
    drop_cols = [
        'Source_IP', 'Destination_IP', 'Source_port', 'Destination_port', 
        'Timestamp', 'label', 'attribution', 'prediction'
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    
    # Encode Protocol
    if 'Protocol' in df.columns:
        df['Protocol'] = df['Protocol'].map({'tcp': 6, 'udp': 17}).fillna(0)
        
    # FIll Missing Values
    df = df.fillna(0)
    
    return df