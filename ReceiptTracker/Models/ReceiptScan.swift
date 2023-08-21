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

struct Receipt: Codable, Identifiable {
    var id: UUID
    var cameraScan: [String]
    
    init(id: UUID = UUID(), cameraScan: [String]) {
        self.id = id
        self.cameraScan = cameraScan
    }
    
    // convert VNDoc and get the uiimage and convert to base64 string
    init(id: UUID = UUID(), cameraScan: VNDocumentCameraScan) {
        self.id = id
        self.cameraScan = (0..<cameraScan.pageCount).map { page in
            let imageData = cameraScan.imageOfPage(at: page).pngData()!
            let strBase64 = imageData.base64EncodedString(options: .lineLength64Characters)
            return strBase64
        }
    }
}
