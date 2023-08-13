//
//  ScanData.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-02.
//

import Foundation

struct ScanData: Identifiable {
    
    let id: UUID
    let content: String
    
    init(id: UUID = UUID(), content: String) {
        self.id = id
        self.content = content
    }
}
