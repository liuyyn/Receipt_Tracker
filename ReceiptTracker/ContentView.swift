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
    @State private var texts: [ScanData] = []
    @State private var scans: [ReceiptScan] = []

    var body: some View {
        NavigationStack {
            VStack {
                
                // display the list of receipts if there are any
//                if texts.count > 0 {
//                    List {
//                        ForEach(texts) { text in
//                            NavigationLink(destination: ScrollView {
//                                Text(text.content)
//                            }, label: {
//                                Text(text.content).lineLimit(1)
//                            })
//                        }
//                    }
//                }
//                else {
//                    Text("No receipts yet")
//                }
                
                if scans.count > 0 {
                    
//                    Image(uiImage: scans[0].cameraScan[0])
                   
                    List($scans) { $scan in
                        
                            NavigationLink(destination: ReceiptView(receipt: $scan)){
                                Text(scan.id.uuidString)
                        
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
            self.scans.append(ReceiptScan(cameraScan: scan))
        })
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
