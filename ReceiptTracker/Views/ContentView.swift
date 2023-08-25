//
//  ContentView.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-07-22.
//

import SwiftUI
import VisionKit

struct ContentView: View {
    @State private var showScannerSheet = false
    @State var texts: [ScanData] = []
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        NavigationStack {
            VStack {
                
                if appState.store.receipts.count > 0 {
//                    List($receipts) { $receipt in
//                        NavigationLink(destination: ReceiptView(receipt: $receipt)) {
//                            Text(receipt.id.uuidString)
//                        }
//                    }
                    List($appState.store.receipts){ $receipt in
                        NavigationLink(destination: ReceiptView(receipt: $receipt)) {
                            Text(receipt.id.uuidString)
                        }
                    }
                }
                else {
                    Text("no receipts")
                }
            }
            .navigationTitle("Scan Receipt")
            .navigationBarItems(trailing: Button(action: {
                showScannerSheet = true
            }, label: { Image(systemName: "doc.text.viewfinder")
                    .font(.title)
            }))
            .sheet(isPresented: $showScannerSheet) {
                makeScannerView()
            }
        }
    }
    private func makeScannerView() -> ScannerView {
        ScannerView(completion: {textPerPage in
            if let outputText = textPerPage?.joined(separator: "\n").trimmingCharacters(in: .whitespacesAndNewlines) {
                
                let newScanData = ScanData(content: outputText)
                self.texts.append(newScanData)
            }
            self.showScannerSheet = false
        }, saveReceipts: { scan in
            //append the new receipt to the state and save to db
            appState.saveReceipt(receipt: Receipt(cameraScan: scan))
        })
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
