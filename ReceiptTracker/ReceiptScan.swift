//
//  ReceiptScan.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-09.
//

import Foundation
import Vision
import VisionKit
import SwiftUI

class ReceiptScan: Identifiable, ObservableObject {
    var id: UUID
    @Published var cameraScan: [UIImage]
    
    init(id: UUID = UUID(), cameraScan: VNDocumentCameraScan) {
        self.cameraScan = (0..<cameraScan.pageCount).map { page in
            cameraScan.imageOfPage(at: page)
        }
        self.id = id
    }
}
