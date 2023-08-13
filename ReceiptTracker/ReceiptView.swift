//
//  ReceiptView.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-10.
//

import SwiftUI

struct ReceiptView: View {
    @Binding var receipt: ReceiptScan
    
    var body: some View {
        ScrollView {
            VStack {
                ForEach(0..<receipt.cameraScan.count) { page in
                        Image(uiImage: receipt.cameraScan[page])
                }
            }
        }
    }
}
