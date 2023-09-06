//
//  ScannerView.swift
//  ReceiptTracker
//
//  Created by Yu Yun Liu on 2023-08-02.
//

import SwiftUI
import VisionKit

struct ScannerView: UIViewControllerRepresentable {
    
    typealias UIViewControllerType = VNDocumentCameraViewController
    private let completionHandler: ([String]?) -> Void // takes optional set of string and return void
    private let saveReceipts: (VNDocumentCameraScan, [String]?) -> Void // saves the images and store them in ContentView variable allocated for that
    
    init(completion: @escaping ([String]?) -> Void, saveReceipts: @escaping (VNDocumentCameraScan, [String]?) -> Void) {
        self.completionHandler = completion
        self.saveReceipts = saveReceipts
    }
    
    func makeUIViewController(context: Context) -> VNDocumentCameraViewController {
        let viewController = VNDocumentCameraViewController()
        viewController.delegate = context.coordinator
        return viewController
    }
    
    func updateUIViewController(_ uiViewController: VNDocumentCameraViewController, context: Context) {
    }
    
    func makeCoordinator() -> Coordinator {
        return Coordinator(completion: completionHandler, saveReceipts: saveReceipts)
    }
    
    final class Coordinator: NSObject, VNDocumentCameraViewControllerDelegate {
        private let completionHandler: ([String]?) -> Void
        private let saveReceipts: (VNDocumentCameraScan, [String]?) -> Void
        
        init(completion: @escaping ([String]?) -> Void, saveReceipts: @escaping (VNDocumentCameraScan, [String]?) -> Void) {
            self.completionHandler = completion
            self.saveReceipts = saveReceipts
        }
        
        func documentCameraViewController(_ controller: VNDocumentCameraViewController, didFinishWith scan: VNDocumentCameraScan) {
            let recognizer = TextRecognizer(cameraScan: scan)
            let textPerPage = recognizer.recognizeText(withCompletionHandler: completionHandler)
            // save the images
            DispatchQueue.main.async {
                self.saveReceipts(scan, textPerPage)
            }
        }
        
        func documentCameraViewController(_ controller: VNDocumentCameraViewController, didFailWithError error: Error) {
            completionHandler(nil)
        }
        
        func documentCameraViewControllerDidCancel(_ controller: VNDocumentCameraViewController) {
            completionHandler(nil)
        }
    }
}
 
