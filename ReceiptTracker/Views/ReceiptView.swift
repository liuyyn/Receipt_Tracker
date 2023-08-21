//
//  ReceiptView.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-10.
//

import SwiftUI

struct ReceiptView: View {
    @Binding var receipt: Receipt
    
    func getUIImage(strBase64: String) -> UIImage {
        let dataDecoded:Data = Data(base64Encoded: strBase64, options: .ignoreUnknownCharacters)!
        if let decodedImage = UIImage(data: dataDecoded) {
            return decodedImage
        }
        return UIImage()
    }
    
    var body: some View {
        ScrollView {
            VStack {
                ForEach(0..<receipt.cameraScan.count, id: \.self) { page in
                        Image(uiImage: getUIImage(strBase64: receipt.cameraScan[page]))
                        .resizable()
                        .scaledToFit()
                }
            }
        }
    }
}
