#!/usr/bin/env swift

import AppKit
import Foundation

struct Options {
    var format = "png"
    var outputDirectory = "/private/tmp"
    var prefix = "claude_clipboard_image"
}

func printUsageAndExit(_ code: Int32 = 0) -> Never {
    let usage = """
    Usage:
      fix-claude-clipboard-image.swift [--format png|jpg] [--out-dir DIR] [--prefix NAME]

    Reads the current macOS clipboard image, re-encodes it into a real PNG/JPEG file,
    saves it to disk, and copies the generated file path back to the clipboard.

    Default:
      --format png
      --out-dir /private/tmp
      --prefix claude_clipboard_image
    """
    fputs(usage + "\n", code == 0 ? stdout : stderr)
    exit(code)
}

func parseOptions() -> Options {
    var options = Options()
    var args = Array(CommandLine.arguments.dropFirst())

    while !args.isEmpty {
        let arg = args.removeFirst()
        switch arg {
        case "--help", "-h":
            printUsageAndExit()
        case "--format", "-f":
            guard !args.isEmpty else {
                fputs("Missing value for \(arg)\n", stderr)
                printUsageAndExit(2)
            }
            let value = args.removeFirst().lowercased()
            guard ["png", "jpg", "jpeg"].contains(value) else {
                fputs("Unsupported format: \(value). Use png or jpg.\n", stderr)
                printUsageAndExit(2)
            }
            options.format = value == "jpeg" ? "jpg" : value
        case "--out-dir", "-o":
            guard !args.isEmpty else {
                fputs("Missing value for \(arg)\n", stderr)
                printUsageAndExit(2)
            }
            options.outputDirectory = NSString(string: args.removeFirst()).expandingTildeInPath
        case "--prefix", "-p":
            guard !args.isEmpty else {
                fputs("Missing value for \(arg)\n", stderr)
                printUsageAndExit(2)
            }
            options.prefix = args.removeFirst()
        default:
            fputs("Unknown argument: \(arg)\n", stderr)
            printUsageAndExit(2)
        }
    }

    return options
}

func imageFromClipboard() -> NSImage? {
    let pasteboard = NSPasteboard.general

    let imageTypes = [
        NSPasteboard.PasteboardType("public.png"),
        NSPasteboard.PasteboardType("Apple PNG pasteboard type"),
        NSPasteboard.PasteboardType("public.tiff"),
        NSPasteboard.PasteboardType("NeXT TIFF v4.0 pasteboard type"),
        NSPasteboard.PasteboardType("public.jpeg"),
        NSPasteboard.PasteboardType("public.jpg")
    ]

    for type in imageTypes {
        if let data = pasteboard.data(forType: type), let image = NSImage(data: data) {
            return image
        }
    }

    if let images = pasteboard.readObjects(forClasses: [NSImage.self], options: nil) as? [NSImage],
       let image = images.first {
        return image
    }

    let urlOptions: [NSPasteboard.ReadingOptionKey: Any] = [
        .urlReadingFileURLsOnly: true
    ]
    if let urls = pasteboard.readObjects(forClasses: [NSURL.self], options: urlOptions) as? [URL] {
        for url in urls {
            if let image = NSImage(contentsOf: url) {
                return image
            }
        }
    }

    return nil
}

func bitmapRepresentation(from image: NSImage) -> NSBitmapImageRep? {
    if let tiff = image.tiffRepresentation,
       let rep = NSBitmapImageRep(data: tiff) {
        return rep
    }

    guard let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        return nil
    }

    return NSBitmapImageRep(cgImage: cgImage)
}

func encodedData(from image: NSImage, format: String) -> Data? {
    guard let rep = bitmapRepresentation(from: image) else {
        return nil
    }

    if format == "jpg" {
        return rep.representation(using: .jpeg, properties: [.compressionFactor: 0.95])
    }

    return rep.representation(using: .png, properties: [:])
}

func copyPathToClipboard(_ path: String) {
    let pasteboard = NSPasteboard.general
    pasteboard.clearContents()
    pasteboard.setString(path, forType: .string)
}

let options = parseOptions()

guard let image = imageFromClipboard() else {
    fputs("No image found in clipboard. Copy a screenshot or image first.\n", stderr)
    exit(1)
}

guard let data = encodedData(from: image, format: options.format) else {
    fputs("Could not encode clipboard image as \(options.format).\n", stderr)
    exit(1)
}

let fileManager = FileManager.default
try fileManager.createDirectory(
    atPath: options.outputDirectory,
    withIntermediateDirectories: true
)

let timestamp = Int(Date().timeIntervalSince1970)
let ext = options.format == "jpg" ? "jpg" : "png"
let fileName = "\(options.prefix)-\(timestamp).\(ext)"
let outputURL = URL(fileURLWithPath: options.outputDirectory).appendingPathComponent(fileName)

do {
    try data.write(to: outputURL, options: [.atomic])
    copyPathToClipboard(outputURL.path)
    print(outputURL.path)
} catch {
    fputs("Could not write image: \(error.localizedDescription)\n", stderr)
    exit(1)
}
